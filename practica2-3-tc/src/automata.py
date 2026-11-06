class Automata:
    def __init__(self, tipo, alfabeto, estados, inicial, aceptacion, transiciones):
        self.tipo = tipo
        self.alfabeto = set(alfabeto)
        self.estados = set(estados)
        self.inicial = inicial
        self.aceptacion = set(aceptacion)
        self.transiciones = {}
        for (desde, lee), destinos in transiciones.items():
            if isinstance(destinos, set):
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
        """Transforma un AFN-lambda en un AFN sin transiciones lambda (Ejercicio 2.2)."""
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
        """Transforma un AFN en un AFD equivalente mediante subconjuntos (Ejercicio 2.3)."""
        auto_base = self.eliminar_transiciones_lambda() if self.tipo == 'AFND-lambda' else self
        
        inicial_set = frozenset(auto_base.clausura_lambda(auto_base.inicial)) if auto_base.tipo == 'AFND-lambda' else frozenset([auto_base.inicial])
        
        pendientes = [inicial_set]
        subconjuntos_map = {inicial_set: "D0"}
        contador = 1
        
        nuevos_estados = {"D0"}
        nuevos_transiciones = {}
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
                    nuevos_transiciones[(nombre_actual, simbolo)] = nombre_destino
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
            transiciones=nuevos_transiciones
        )
        return afd_resultado, tabla_pasos

    def minimizar_afd(self):
        """Obtiene el AFD mínimo por refinamiento de particiones (Ejercicio 2.4)."""
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

    def simular_cadena(self, cadena):
        """Simula una cadena y retorna (aceptada: bool, traza: list)"""
        traza = []
        
        if self.tipo in ['AFD', 'AFND']:
            estado_actual = self.inicial
            traza.append({estado_actual})
            
            for simbolo in cadena:
                if simbolo not in self.alfabeto:
                    return False, traza
                
                key = (estado_actual, simbolo)
                if key in self.transiciones:
                    destinos = self.transiciones[key]
                    if isinstance(destinos, (set, frozenset)):
                        estado_actual = list(destinos)[0]
                    else:
                        estado_actual = destinos
                    traza.append({estado_actual})
                else:
                    return False, traza
            
            aceptada = estado_actual in self.aceptacion
            return aceptada, traza

        elif self.tipo == 'AFND-lambda':
            current_states = self.clausura_lambda(self.inicial)
            traza.append(set(current_states))
            
            for simbolo in cadena:
                if simbolo not in self.alfabeto:
                    return False, traza
                
                siguientes = set()
                for est in current_states:
                    key = (est, simbolo)
                    if key in self.transiciones:
                        for destino in self.transiciones[key]:
                            siguientes.update(self.clausura_lambda(destino))
                
                current_states = frozenset(siguientes)
                traza.append(set(current_states))
                
            aceptada = any(est in self.aceptacion for est in current_states)
            return aceptada, traza

        return False, traza