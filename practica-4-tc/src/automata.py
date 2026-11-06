class NFAFragment:
    def __init__(self, start, accept, transitions, states):
        self.start = start
        self.accept = accept
        self.transitions = transitions  # {(desde, lee): set(destinos)}
        self.states = states            # set de estados

class Automata:
    def __init__(self, tipo, alfabeto, estados, inicial, aceptacion, transiciones):
        self.tipo = tipo
        self.alfabeto = set(alfabeto)
        self.estados = set(estados)
        self.inicial = inicial
        self.aceptacion = set(aceptacion)
        self.transiciones = {}
        for (desde, lee), destinos in transiciones.items():
            if isinstance(destinos, (set, frozenset)):
                self.transiciones[(desde, lee)] = frozenset(destinos)
            elif isinstance(destinos, (list, tuple)):
                self.transiciones[(desde, lee)] = frozenset(destinos)
            else:
                self.transiciones[(desde, lee)] = frozenset([destinos])

    def clausura_lambda(self, estados):
        """Calcula la cerradura lambda (épsilon-clausura) para un estado o conjunto de estados."""
        actuales = set(estados) if isinstance(estados, (set, frozenset)) else {estados}
        sonda = list(actuales)
        while sonda:
            est = sonda.pop()
            for simbolo in ['', 'lambda', 'ε']:
                key = (est, simbolo)
                if key in self.transiciones:
                    for destino in self.transiciones[key]:
                        if destino not in actuales:
                            actuales.add(destino)
                            sonda.append(destino)
        return frozenset(actuales)

    def eliminar_transiciones_lambda(self):
        """Transforma un AFN-lambda en un AFN sin transiciones lambda."""
        if self.tipo != 'AFND-lambda':
            return self 

        nuevas_transiciones = {}
        nuevos_aceptacion = set()

        for est in self.estados:
            clausura = self.clausura_lambda(est)
            if any(a in self.aceptacion for a in clausura):
                nuevos_aceptacion.add(est)

        for est in self.estados:
            clausura_est = self.clausura_lambda(est)
            for simbolo in self.alfabeto:
                destinos_simbolo = set()
                for e in clausura_est:
                    key = (e, simbolo)
                    if key in self.transiciones:
                        destinos_simbolo.update(self.transiciones[key])
                
                destinos_finales = set()
                for d in destinos_simbolo:
                    destinos_finales.update(self.clausura_lambda(d))
                
                if destinos_finales:
                    nuevas_transiciones[(est, simbolo)] = frozenset(destinos_finales)

        return Automata(
            tipo='AFND' if any(len(v) > 1 for v in nuevas_transiciones.values()) else 'AFD',
            alfabeto=self.alfabeto,
            estados=self.estados,
            inicial=self.inicial,
            aceptacion=nuevos_aceptacion,
            transiciones=nuevas_transiciones
        )

    def construir_afd_subconjuntos(self):
        """Transforma un AFN en un AFD equivalente mediante construcción de subconjuntos."""
        auto_base = self.eliminar_transiciones_lambda() if self.tipo == 'AFND-lambda' else self
        
        inicial_set = frozenset(auto_base.clausura_lambda(auto_base.inicial)) if auto_base.tipo == 'AFND-lambda' else frozenset([auto_base.inicial])
        
        pendientes = [inicial_set]
        subconjuntos_map = {inicial_set: "D0"}
        contador = 1
        
        nuevos_estados = {"D0"}
        nuevas_transiciones = {}
        nuevos_aceptacion = set()
        
        if any(e in auto_base.aceptacion for e in inicial_set):
            nuevos_aceptacion.add("D0")
            
        tabla_pasos = []

        while pendientes:
            actual_set = pendientes.pop(0)
            nombre_actual = subconjuntos_map[actual_set]
            
            fila_tabla = {"estado": nombre_actual, "subconjunto": set(actual_set), "transiciones": {}}
            
            for simbolo in sorted(auto_base.alfabeto):
                siguientes = set()
                for est in actual_set:
                    key = (est, simbolo)
                    if key in auto_base.transiciones:
                        siguientes.update(auto_base.transiciones[key])
                
                if siguientes:
                    sig_frozenset = frozenset(siguientes)
                    if sig_frozenset not in subconjuntos_map:
                        nuevo_nombre = f"D{contador}"
                        contador += 1
                        subconjuntos_map[sig_frozenset] = nuevo_nombre
                        nuevos_estados.add(nuevo_nombre)
                        pendientes.append(sig_frozenset)
                        if any(e in auto_base.aceptacion for e in sig_frozenset):
                            nuevos_aceptacion.add(nuevo_nombre)
                    
                    nombre_destino = subconjuntos_map[sig_frozenset]
                    nuevas_transiciones[(nombre_actual, simbolo)] = nombre_destino
                    fila_tabla["transiciones"][simbolo] = nombre_destino
                else:
                    fila_tabla["transiciones"][simbolo] = "-"
            
            tabla_pasos.append(fila_tabla)

        afd_resultado = Automata(
            tipo='AFD',
            alfabeto=auto_base.alfabeto,
            estados=nuevos_estados,
            inicial="D0",
            aceptacion=nuevos_aceptacion,
            transiciones=nuevas_transiciones
        )
        return afd_resultado, tabla_pasos

    @classmethod
    def desde_regex(cls, regex_str):
        """Construye un AFD a partir de una Expresión Regular usando Thompson y Subconjuntos."""
        s = regex_str.replace(" ", "").replace("ε", "").replace("E", "")
        if not s:
            raise ValueError("Expresión regular vacía")

        tokens = []
        for i, c in enumerate(s):
            tokens.append(c)
            if i + 1 < len(s):
                curr = c
                nxt = s[i + 1]
                if curr not in "(+|" and nxt not in ")*+|":
                    tokens.append('.')

        precedencia = {'*': 3, '.': 2, '+': 1, '|': 1}
        output = []
        operators = []

        for token in tokens:
            if token not in ('*', '.', '+', '|', '(', ')'):
                output.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if operators:
                    operators.pop()
            else:
                while (operators and operators[-1] != '(' and
                       precedencia.get(operators[-1], 0) >= precedencia.get(token, 0)):
                    output.append(operators.pop())
                operators.append(token)

        while operators:
            output.append(operators.pop())

        state_counter = 0
        def nuevo_estado():
            nonlocal state_counter
            st = f"q{state_counter}"
            state_counter += 1
            return st

        stack = []
        alfabeto = set()

        for token in output:
            if token not in ('*', '.', '+', '|', '(', ')'):
                alfabeto.add(token)
                s0 = nuevo_estado()
                s1 = nuevo_estado()
                trans = {(s0, token): {s1}}
                frag = NFAFragment(s0, s1, trans, {s0, s1})
                stack.append(frag)
            elif token == '.':
                f2 = stack.pop()
                f1 = stack.pop()
                trans = dict(f1.transitions)
                for k, v in f2.transitions.items():
                    if k in trans:
                        trans[k] = trans[k].union(v)
                    else:
                        trans[k] = v
                key = (f1.accept, '')
                if key in trans:
                    trans[key] = trans[key].union({f2.start})
                else:
                    trans[key] = {f2.start}
                
                estados_totales = f1.states.union(f2.states)
                stack.append(NFAFragment(f1.start, f2.accept, trans, estados_totales))
            elif token in ('+', '|'):
                f2 = stack.pop()
                f1 = stack.pop()
                s0 = nuevo_estado()
                s1 = nuevo_estado()
                trans = dict(f1.transitions)
                for k, v in f2.transitions.items():
                    if k in trans:
                        trans[k] = trans[k].union(v)
                    else:
                        trans[k] = v
                
                trans[(s0, '')] = {f1.start, f2.start}
                trans[(f1.accept, '')] = {s1}
                trans[(f2.accept, '')] = {s1}
                
                estados_totales = f1.states.union(f2.states).union({s0, s1})
                stack.append(NFAFragment(s0, s1, trans, estados_totales))
            elif token == '*':
                f = stack.pop()
                s0 = nuevo_estado()
                s1 = nuevo_estado()
                trans = dict(f.transitions)
                trans[(s0, '')] = {f.start, s1}
                if (f.accept, '') in trans:
                    trans[(f.accept, '')] = trans[(f.accept, '')].union({f.start, s1})
                else:
                    trans[(f.accept, '')] = {f.start, s1}
                
                estados_totales = f.states.union({s0, s1})
                stack.append(NFAFragment(s0, s1, trans, estados_totales))

        if not stack:
            raise ValueError("Expresión regular inválida")

        nfa_final = stack.pop()
        afn_obj = Automata(
            tipo='AFND-lambda',
            alfabeto=alfabeto,
            estados=nfa_final.states,
            inicial=nfa_final.start,
            aceptacion={nfa_final.accept},
            transiciones=nfa_final.transitions
        )

        afd_obj, _ = afn_obj.construir_afd_subconjuntos()
        return afd_obj

    def minimizar_afd(self):
        """Obtiene el AFD mínimo por refinamiento de particiones."""
        alcanzables = {self.inicial}
        sonda = [self.inicial]
        while sonda:
            est = sonda.pop()
            for sim in self.alfabeto:
                key = (est, sim)
                if key in self.transiciones:
                    dest = list(self.transiciones[key])[0]
                    if dest not in alcanzables:
                        alcanzables.add(dest)
                        sonda.append(dest)

        estados_val = sorted(list(alcanzables))
        
        aceptantes = frozenset(e for e in estados_val if e in self.aceptacion)
        no_aceptantes = frozenset(e for e in estados_val if e not in self.aceptacion)
        
        particion = []
        if aceptantes: particion.append(aceptantes)
        if no_aceptantes: particion.append(no_aceptantes)
        
        def encontrar_grupo(estado, part):
            for i, grupo in enumerate(part):
                if estado in grupo:
                    return i
            return -1

        while True:
            nueva_particion = []
            cambio = False
            
            for grupo in particion:
                if len(grupo) <= 1:
                    nueva_particion.append(grupo)
                    continue
                
                subgrupos = {}
                for est in grupo:
                    firma = []
                    for sim in sorted(self.alfabeto):
                        key = (est, sim)
                        dest = list(self.transiciones[key])[0] if key in self.transiciones else None
                        idx_grupo = encontrar_grupo(dest, particion) if dest else -1
                        firma.append(idx_grupo)
                    firma_tuple = tuple(firma)
                    if firma_tuple not in subgrupos:
                        subgrupos[firma_tuple] = set()
                    subgrupos[firma_tuple].add(est)
                
                if len(subgrupos) > 1:
                    cambio = True
                for sg in subgrupos.values():
                    nueva_particion.append(frozenset(sg))
            
            if not cambio:
                break
            particion = nueva_particion

        mapa_grupos = {}
        nuevos_estados = set()
        nuevos_aceptacion = set()
        nuevo_inicial = ""
        nuevas_transiciones = {}

        for i, grupo in enumerate(particion):
            nombre_grupo = f"G{i}"
            nuevos_estados.add(nombre_grupo)
            for est in grupo:
                mapa_grupos[est] = nombre_grupo
                if est == self.inicial:
                    nuevo_inicial = nombre_grupo
                if est in self.aceptacion:
                    nuevos_aceptacion.add(nombre_grupo)

        for i, grupo in enumerate(particion):
            representante = list(grupo)[0]
            nombre_origen = f"G{i}"
            for sim in sorted(self.alfabeto):
                key = (representante, sim)
                if key in self.transiciones:
                    dest_orig = list(self.transiciones[key])[0]
                    dest_grupo = mapa_grupos[dest_orig]
                    nuevas_transiciones[(nombre_origen, sim)] = dest_grupo

        afd_minimo = Automata(
            tipo='AFD',
            alfabeto=self.alfabeto,
            estados=nuevos_estados,
            inicial=nuevo_inicial,
            aceptacion=nuevos_aceptacion,
            transiciones=nuevas_transiciones
        )
        return afd_minimo, particion

    def automata_a_regex_rij(self):
        """Convierte un AFD a ER por eliminación de estados (Rij), simplificando cada paso."""
        from regex_simplifier import EMPTY, EPSILON, literal, union, concat, star, render

        # El método Rij admite cualquier autómata finito; se rechazan transiciones no deterministas
        # solo si el conjunto contiene varios destinos, aunque la fórmula también podría manejarlos.
        estados = sorted(self.estados, key=str)
        s_in, s_acc = "__inicio__", "__aceptacion__"
        todos = [s_in] + estados + [s_acc]
        R = {u: {v: EMPTY for v in todos} for u in todos}
        R[s_in][self.inicial] = EPSILON
        for final in self.aceptacion:
            R[final][s_acc] = union(R[final][s_acc], EPSILON)
        for (origen, simbolo), destinos in self.transiciones.items():
            for destino in destinos:
                R[origen][destino] = union(R[origen][destino], literal(simbolo))

        pasos = []
        for k in estados:
            if k not in R:
                continue
            activos = [x for x in R.keys() if x != k]
            bucle = star(R[k][k])
            nueva = {u: dict(R[u]) for u in R}
            for i in activos:
                if R[i][k] == EMPTY:
                    continue
                for j in activos:
                    if R[k][j] == EMPTY:
                        continue
                    camino = concat(R[i][k], bucle, R[k][j])
                    nueva[i][j] = union(R[i][j], camino)
            # Retirar el estado eliminado de la matriz.
            del nueva[k]
            for fila in nueva.values():
                fila.pop(k, None)
            R = nueva
            snapshot = {
                origen: {destino: render(expr) for destino, expr in fila.items()}
                for origen, fila in R.items()
            }
            pasos.append((k, snapshot))

        resultado = R.get(s_in, {}).get(s_acc, EMPTY)
        return render(resultado), pasos

    def simular_cadena(self, cadena):
        """Simula una cadena en el autómata y retorna (aceptada: bool, traza: list)."""
        traza = []
        
        if self.tipo == 'AFD':
            estado_actual = self.inicial
            traza.append({estado_actual})
            
            for simbolo in cadena:
                if simbolo not in self.alfabeto:
                    return False, traza
                
                key = (estado_actual, simbolo)
                if key in self.transiciones:
                    destinos = self.transiciones[key]
                    estado_actual = list(destinos)[0]
                    traza.append({estado_actual})
                else:
                    return False, traza
            
            aceptada = estado_actual in self.aceptacion
            return aceptada, traza
        else:
            current_states = self.clausura_lambda(self.inicial) if self.tipo == 'AFND-lambda' else frozenset([self.inicial])
            traza.append(set(current_states))
            
            for simbolo in cadena:
                if simbolo not in self.alfabeto:
                    return False, traza
                
                siguientes = set()
                for est in current_states:
                    key = (est, simbolo)
                    if key in self.transiciones:
                        for destino in self.transiciones[key]:
                            si_lambda = self.clausura_lambda(destino) if self.tipo == 'AFND-lambda' else {destino}
                            siguientes.update(si_lambda)
                
                current_states = frozenset(siguientes)
                traza.append(set(current_states))
                
            aceptada = any(est in self.aceptacion for est in current_states)
            return aceptada, traza