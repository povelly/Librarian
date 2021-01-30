try:
    import symbols
    from regex import RegEx
except:
    from Librarian.models import symbols
    from .regex import RegEx


class Arc():
    def __init__(self, symbol, destination):
        self.symbol = symbol
        self.destination = destination

    def __repr__(self):
        return "Arc(" + chr(self.symbol) + " |-> " + str(self.destination) + ")"


class State():
    def __init__(self, arcs, final):
        self.arcs = arcs
        self.final = final

    def __repr__(self):
        res = "State(\n    Arcs: ["
        for i in range(len(self.arcs) - 1):
            res += repr(self.arcs[i]) + ", "
        if len(self.arcs) > 0:
            res += repr(self.arcs[len(self.arcs) - 1])
        res += "]\n    Final : " + str(self.final) + "\n)"
        return res


class Automaton():
    def __init__(self, states, initial_state):
        self.states = states
        self.initial_state = initial_state

    def __repr__(self):
        return "Automaton(\n  States: " + str(self.states) + ",\n Initial_state: " + str(self.initial_state) + "\n)"

    @staticmethod
    def parse_tree(tree):
        initial_state = State([], False)
        final_state = State([], True)
        return Automaton(Automaton.parse_auxiliary(tree, 0, 1, [initial_state, final_state]), 0)

    @staticmethod
    def parse_auxiliary(tree, initial_state, final_state, result):
        if tree.root == symbols.CONCAT:
            state5 = State([], False)
            state6 = State([], False)
            result.extend((state5, state6))
            arc5 = Arc(symbols.EPSILON, result.index(state6))
            state5.arcs.append(arc5)
            # TODO
            tmp = Automaton.parse_auxiliary(
                tree.sub_trees[0], initial_state, result.index(state5), result)
            return Automaton.parse_auxiliary(tree.sub_trees[1], result.index(state6), final_state, tmp)
        elif tree.root == symbols.QUESTION:
            state9 = State([], False)
            state10 = State([], True)
            result.extend((state9, state10))
            arc10 = Arc(symbols.EPSILON, result.index(state9))
            arc11 = Arc(symbols.EPSILON, result.index(state10))
            result[initial_state].final = True
            result[initial_state].arcs.append(arc10)
            state9.arcs.append(arc11)
            return Automaton.parse_auxiliary(tree.sub_trees[0], result.index(state9), result.index(state10), result)
        elif tree.root == symbols.STAR:
            state7 = State([], False)
            state8 = State([], False)
            result.extend((state7, state8))
            arc6 = Arc(symbols.EPSILON, result.index(state7))
            result[initial_state].arcs.append(arc6)
            arc7 = Arc(symbols.EPSILON, final_state)
            state8.arcs.append(arc7)
            arc8 = Arc(symbols.EPSILON, result.index(state7))
            state8.arcs.append(arc8)
            arc9 = Arc(symbols.EPSILON, final_state)
            result[initial_state].arcs.append(arc9)
            return Automaton.parse_auxiliary(tree.sub_trees[0], result.index(state7), result.index(state8), result)
        elif tree.root == symbols.ALTERN:
            state1 = State([], False)  # left-automaton-initial-state
            state2 = State([], False)  # left-automaton-final-state
            state3 = State([], False)  # right-initial
            state4 = State([], False)  # right-final
            result.extend((state1, state2, state3, state4))
            arc2 = Arc(symbols.EPSILON, final_state)
            state2.arcs.append(arc2)
            arc4 = Arc(symbols.EPSILON, final_state)
            state4.arcs.append(arc4)
            arc1 = Arc(symbols.EPSILON, result.index(state1))
            result[initial_state].arcs.append(arc1)
            arc3 = Arc(symbols.EPSILON, result.index(state3))
            result[initial_state].arcs.append(arc3)
            # TODO
            tmp = Automaton.parse_auxiliary(
                tree.sub_trees[0], result.index(state1), result.index(state2), result)
            return Automaton.parse_auxiliary(tree.sub_trees[1], result.index(state3), result.index(state4), tmp)
        elif tree.root == symbols.DOT:  # TODO
            return ""
        else:
            result[initial_state].arcs.append(Arc(tree.root, final_state))
            return result

    @staticmethod
    def dfs(node, matrix):
        reachable = []
        to_be_visited = []
        to_be_visited.append(node)
        while len(to_be_visited) > 0:
            visit = to_be_visited.pop()
            for j in range(len(matrix)):
                if matrix[visit][j] == 1:
                    if j != visit:
                        to_be_visited.append(j)
                    if not j in reachable:
                        reachable.append(j)
        return reachable

    @staticmethod
    def reduce_automaton(automaton):
        # Step 1
        epsilon_auto = []
        for s in automaton.states:
            state1 = State([], False)
            for a in s.arcs:
                if a.symbol == symbols.EPSILON:
                    arc = Arc(a.symbol, a.destination)
                    state1.arcs.append(arc)
            epsilon_auto.append(state1)

        # Step 2
        matrix = [0] * len(automaton.states)
        for i in range(len(matrix)):
            matrix[i] = [0] * len(matrix)
            matrix[i][i] = 1
            for j in range(len(matrix)):
                for a in epsilon_auto[i].arcs:
                    if a.destination == j:
                        matrix[i][j] = 1

        # Step 3
        auto_res = [State([], True)]
        a_visiter = [0]

        while len(a_visiter) > 0:
            visit = a_visiter.pop()
            accessible = Automaton.dfs(visit, matrix)
            auto_res = Automaton.resize_auto(auto_res, visit)
            auto_res[visit] = State([], False)
            for s in accessible:
                if automaton.states[s].final:
                    auto_res[visit].final = True
                for a in automaton.states[s].arcs:
                    if a.symbol != symbols.EPSILON:
                        if a.destination != visit:
                            a_visiter.append(a.destination)
                        arc = Arc(a.symbol, a.destination)
                        auto_res[visit].arcs.append(arc)
        return Automaton(auto_res, 0)

    @staticmethod
    def resize_auto(auto_res, indice_max):
        while len(auto_res) < indice_max + 1:
            auto_res.append(None)
        return auto_res

    @staticmethod
    def ligne_id(tab_auto, id):
        for i in range(len(tab_auto)):
            if tab_auto[i][0] == id:
                return i
        # raise Exception("Can't get id")
        return -1  # Error

    @staticmethod
    def reduce_automaton2(automaton):
        # Step 1
        tab_auto = []
        i = 0
        for s in automaton.states:
            if s is not None:
                # tab_auto[i] = []
                if len(tab_auto) == i:
                    tab_auto.append([None] * 260)
                tab_auto[i][0] = automaton.states.index(s)
                if automaton.initial_state == automaton.states.index(s):
                    tab_auto[i][257] = 1
                else:
                    tab_auto[i][257] = 0
                if s.final:
                    tab_auto[i][258] = 1
                else:
                    tab_auto[i][258] = 0
                tab_auto[i][259] = True
                i += 1
        state = len(automaton.states) + 1
        tab_auto = Automaton.resize_auto(tab_auto, i)
        # tab_auto[i] = []
        tab_auto[i] = [None] * 259
        tab_auto[i][0] = state
        tab_auto[i][257] = 0
        tab_auto[i][258] = 0
        for j in range(1, 257):
            tab_auto[i][j] = state
        i = 0
        for s in automaton.states:
            if s is not None:
                for j in range(1, 257):
                    tab_auto[i][j] = state
                for a in s.arcs:
                    tab_auto[i][a.symbol + 1] = a.destination
                i += 1

        # Step 2
        matrix_equi = []
        for k in range(len(tab_auto)):
            # matrix_equi[k] = []
            matrix_equi.append([])
            for l in range(len(tab_auto)):
                matrix_equi[k].append(None)
                if k == l:
                    matrix_equi[k][l] = 1
                else:
                    if k > l:
                        matrix_equi[k][l] = -1
                        continue
                    else:
                        if tab_auto[k][258] != tab_auto[l][258] or l == len(tab_auto) - 1:
                            matrix_equi[k][l] = 0
                        else:
                            matrix_equi[k][l] = 2

        # Step 3
        modification = True
        while modification:
            modification = False
            for i in range(len(matrix_equi)):
                for j in range(len(matrix_equi)):
                    if matrix_equi[i][j] == -1 or matrix_equi[i][j] == 0 or matrix_equi[i][j] == 1:
                        continue
                    equiv = True
                    for k in range(1, 257):
                        k1 = tab_auto[i][k]
                        k2 = tab_auto[j][k]
                        ik1 = Automaton.ligne_id(tab_auto, k1)
                        ik2 = Automaton.ligne_id(tab_auto, k2)
                        if ik1 > ik2:
                            tmp = ik1
                            ik1 = ik2
                            ik2 = tmp
                        if matrix_equi[ik1][ik2] == 0:
                            matrix_equi[i][j] = 0
                            modification = True
                            equiv = False
                            break
                        if matrix_equi[ik1][ik2] == 2:
                            equiv = False
                            break
                        if matrix_equi[ik1][ik2] == 1:
                            continue

        # Finalisation
        for i in range(len(matrix_equi)):
            for j in range(len(matrix_equi)):
                if matrix_equi[i][j] == 2:
                    matrix_equi[i][j] = 1

        # Step 4
        fusion = False
        for i in range(len(matrix_equi)):
            for j in range(len(matrix_equi)):
                if matrix_equi[i][j] == 1 and i != j:
                    fusion = True
                    for k in range(len(tab_auto)):
                        for l in range(1, 257):
                            if tab_auto[k][l] == tab_auto[j][0]:
                                tab_auto[k][l] = tab_auto[i][0]
                    for k in range(1, 257):
                        if tab_auto[j][k] != state:
                            if tab_auto[j][k] == j:
                                tab_auto[i][k] = i
                            else:
                                tab_auto[i][k] = tab_auto[j][k]
                    tab_auto[j][259] = False

        auto2 = Automaton([], 0)

        for i in range(len(tab_auto) - 1):
            if tab_auto[i][259] and i != Automaton.ligne_id(tab_auto, state):
                state2 = State([], tab_auto[i][258])
                for j in range(1, 257):
                    if tab_auto[i][j] != state:
                        arc = Arc(j - 1, tab_auto[i][j])
                        state2.arcs.append(arc)
                auto2.states = Automaton.resize_auto(
                    auto2.states, tab_auto[i][0])
                auto2.states[tab_auto[i][0]] = state2

        return auto2

    @staticmethod
    def dfa(regex):
        tt = RegEx(regex).parsex()
        auto_res = Automaton.parse_tree(tt)
        auto_e1 = Automaton.reduce_automaton(auto_res)
        auto2 = Automaton.reduce_automaton2(auto_e1)
        auto2.cleanUp()
        return auto2

    def cleanUp(self):
        def clean_aux(automaton, id):
            for s in automaton.states:
                if s is None:
                    continue
                for a in s.arcs:
                    if a.destination > id:
                        a.destination -= 1
        i = 0
        fini = False
        while not fini:
            if self.states[i] is None:
                clean_aux(self, i)
                self.states.pop(i)
                i -= 1

            i += 1
            if i >= len(self.states):
                fini = True

    def walk(self, indexing):
        state_id = self.initial_state
        occurences = 0
        # pour chaque mot de la table d'index
        for word in indexing:
            # on ce place sur l'état initial
            state_id = self.initial_state
            # on lit les caractères du mort
            for i in range(len(word)):
                # si l'automate arrive dans un état final c'est bon
                if self.states[state_id].final:
                    occurences += 1
                    break
                # si on a dépassé la taille du mot, on ne peut pas lire de nouveau caractère
                if i >= len(word):
                    break
                # sinon on doit lire le caractère actuel
                # on recupere le caractere actuel
                c = word[i]
                gotTransition = False
                # on parcours les transitions de l'état actuel
                for a in self.states[state_id].arcs:
                    # une transition existe pour le caractère
                    if a.symbol == ord(c):
                        # on suit la transition
                        gotTransition = True
                        state_id = a.destination
                        break
                # si aucune transition n'existe pour le caractère, le mot est invalide
                if not gotTransition:
                    break
        return occurences

        # state_id = self.initial_state
        # occurences = 0
        # for i in range(len(text) + 1):
        #     if self.states[state_id].final:
        #         occurences += 1
        #         state_id = self.initial_state
        #     if i == len(text):
        #         break
        #     c = text[i]
        #     partially_good = False
        #     for a in self.states[state_id].arcs:
        #         if a.symbol == ord(c):
        #             state_id = a.destination
        #             partially_good = True
        #             break
        #     if not partially_good:
        #         state_id = self.initial_state
        # return occurences


if __name__ == "__main__":
    """
    r = RegEx("a|bc*")
    tt = r.parsex()
    # print(repr(tt))
    auto = Automaton.parse_tree(tt)
    # print(repr(auto))
    auto_epsilon = Automaton.reduce_automaton(auto)
    # print(repr(auto_epsilon))
    dfa = Automaton.reduce_automaton2(auto_epsilon)
    # print(repr(dfa))
    """

    # a = Automaton.dfa("S(a|e|i)rgon")
    # print(a)
    # print("nb d'occurences: " + str(a.walk("SargonSargon")))

    # r2 = RegEx("c?")
    # tt2 = r2.parsex()
    # print(repr(tt2))

    b = Automaton.dfa("c?")
    print(b)
