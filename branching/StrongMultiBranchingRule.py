from pyscipopt import Branchrule, SCIP_RESULT, SCIP_LPSOLSTAT, quicksum
from itertools import combinations
import math

debug = False

class StrongMultiBranchingRule(Branchrule):

    def __init__(self, scip, n):
        self.scip = scip
        self.n = n

    def multiBranchVarVal(self, branch_cands, sum):
        """
        Branch on a set of variables. Specifically, it creates a down and a up
        child node with constraint sum(x_i) <= floor(x*) and sum(x_i) >= ceil(x*),
        respectively, where x* is the sum of x_i's LP solution values.
        """
        assert not self.scip.isFeasIntegral(sum), f"Sum {sum} is not fractional"

        sum_floor = math.floor(sum)

        if sum_floor == 0:
            # This special case implies x_i <= 0 for all i for the down child.
            child_down = self.scip.createChild(0, 0.0)
            for cand in branch_cands:
                self.scip.chgVarUbNode(child_down, cand, 0)

            child_up = self.scip.createChild(0, 0.0)
            cons_up = self.scip.createConsFromExpr(
                quicksum(branch_cands) >= 1,
                local=True,
                # removable=True,
                # propagate=True,
                # stickingatnode=True
            )
            self.scip.addConsNode(child_up, cons_up)

        elif sum_floor + 1 == len(branch_cands):
            # This special case implies x_i <= 0 for all i for the up child.
            child_down = self.scip.createChild(0, 0.0)
            cons_down = self.scip.createConsFromExpr(
                quicksum(branch_cands) <= sum_floor,
                local=True,
                # removable=True,
                # propagate=True,
                # stickingatnode=True
            )
            self.scip.addConsNode(child_down, cons_down)

            child_up = self.scip.createChild(0, 0.0)
            for cand in branch_cands:
                self.scip.chgVarLbNode(child_up, cand, 1)

        else:
            child_down = self.scip.createChild(0, 0.0)
            cons_down = self.scip.createConsFromExpr(
                quicksum(branch_cands) <= sum_floor,
                local=True,
                # removable=True,
                # propagate=True,
                # stickingatnode=True
            )
            self.scip.addConsNode(child_down, cons_down)

            child_up = self.scip.createChild(0, 0.0)
            cons_up = self.scip.createConsFromExpr(
                quicksum(branch_cands) >= sum_floor + 1,
                local=True,
                # removable=True,
                # propagate=True,
                # stickingatnode=True
            )
            self.scip.addConsNode(child_up, cons_up)

        return child_down, None, child_up

    def branchexeclp(self, allowaddcons):
        # Get branching candidates
        branch_cands, branch_cand_sols, branch_cand_fracs, \
            ncands, npriocands, nimplcands = self.scip.getLPBranchCands()

        # NOTE: 'nvar' is in fact the number of items 'n' (if no transformation occurs)
        nvar = self.scip.getNVars()
        vars = self.scip.getVars()
        vals = [self.scip.getSolVal(None, var) for var in vars]

        if ((npriocands == 1) and (self.n == 1)):
            self.scip.branchVarVal(branch_cands[0], branch_cand_sols[0])
            return {"result": SCIP_RESULT.BRANCHED}

        if debug: print("branch_cand_sols = ", branch_cand_sols)
        if debug: print("sense : ", self.scip.getObjectiveSense())

        lpobjval = self.scip.getLPObjVal()
        if debug: print(self.scip.getConss())

        if debug: print("lpobjval = ", lpobjval)
        if debug: print("Primal bound = ", self.scip.getPrimalbound())
        if debug: print("Dual bound = ", self.scip.getDualbound())

        best_score = -self.scip.infinity()
        best_set = None
        best_sum = None
        best_bound_down = None
        best_bound_up = None

        real_n = nvar if (nvar < self.n) else self.n

        if debug: print("n = ", self.n)
        if debug: print("npriocands = ", npriocands)
        if debug: print("n_real = ", real_n)

        if debug: print("START LOOP")
        cand_indices = list(range(nvar))
        # NOTE: we only need the combination with at least one fractional variable
        for idx_set in combinations(cand_indices, real_n):
            var_set = [vars[i] for i in idx_set]
            s = sum(vals[i] for i in idx_set)

            if debug: print(f"iter: {idx_set} = {var_set}, sum = {s}")

            if abs(s - round(s)) < 1e-6:
                continue

            s_floor = math.floor(s)
            s_ceil = math.ceil(s)

            # ---- Down branch ----
            self.scip.startProbing()
            cons_down = self.scip.createConsFromExpr(quicksum(var_set) <= s_floor, local=True)
            self.scip.addConsLocal(cons_down)
            self.scip.constructLP()
            self.scip.solveProbingLP(itlim=200)
            down_inf = (self.scip.getLPSolstat() != SCIP_LPSOLSTAT.OPTIMAL)
            bound_down = None if down_inf else self.scip.getLPObjVal()
            self.scip.endProbing()

            # ---- Up branch ----
            self.scip.startProbing()
            cons_up = self.scip.createConsFromExpr(quicksum(var_set) >= s_ceil, local=True)
            self.scip.addConsLocal(cons_up)
            self.scip.constructLP()
            self.scip.solveProbingLP(itlim=200)
            up_inf = (self.scip.getLPSolstat() != SCIP_LPSOLSTAT.OPTIMAL)
            bound_up = None if up_inf else self.scip.getLPObjVal()
            self.scip.endProbing()

            if down_inf and up_inf:
                return {"result": SCIP_RESULT.CUTOFF}

            if not down_inf:
                down_gain = max([bound_down - lpobjval, 0])
            else:
                down_gain = 0
            if not up_inf:
                up_gain = max([bound_up - lpobjval, 0])
            else:
                up_gain = 0

            if debug: print(f"down inf = {down_inf}, up inf = {up_inf}")
            if debug: print(f"bound_down = {bound_down}, bound_up = {bound_up}")
            if debug: print(f"down gain = {down_gain}, up gain = {up_gain}")

            score = max(down_gain, up_gain)
            # score = self.scip.getBranchScoreMultiple(branch_cands[idx_set], [down_gain, up_gain])
            if debug: print(f"score = {score}")

            if score > best_score:
                best_score = score
                best_set = idx_set
                best_sum = s
                best_down_bound = bound_down
                best_up_bound = bound_up
        if debug: print("END LOOP")

        if best_set is None:
            if debug: print("SCIP RESULT DIDNOTRUN")
            return {"result": SCIP_RESULT.DIDNOTRUN}

        if debug: print("best set = ", best_set)
        if debug: print("best sum = ", best_sum)

        child_down, child_eq, child_up = self.multiBranchVarVal(
            [vars[i] for i in best_set], best_sum)

        # Update the bounds of the down node and up node. Some cols might not exist due to pricing
        if self.scip.allColsInLP():
            if child_down is not None and best_down_bound is not None:
                self.scip.updateNodeLowerbound(child_down, best_down_bound)
            if child_up is not None and best_up_bound is not None:
                self.scip.updateNodeLowerbound(child_up, best_up_bound)

        if debug: print("\n")

        return {"result": SCIP_RESULT.BRANCHED}

if __name__ == "__main__":
    print("hello, world")
