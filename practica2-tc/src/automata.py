class Automata:
    def __init__(self, tipo, alfabeto, estados, inicial, aceptacion, transiciones):
        self.tipo = tipo
        self.alfabeto = set(alfabeto)
        self.estados = set(estados)
        self.inicial = inicial
        self.aceptacion = set(aceptacion)
        # Normalizar transiciones para asegurar claves y valores consistentes
        self.transiciones = {}
        for (desde, lee), destinos in transiciones.items():
            if isinstance(destinos, set):
                self.transiciones[(desde, lee)] = frozenset(destinos)
            elif isinstance(destinos, (list, tuple)):
                self.transiciones[(desde, lee)] = frozenset(destinos)
            else:
                self.transiciones[(desde, lee)] = frozenset([destinos])

    def _clausura_lambda(self, estados):
        """Calcula la clausura lambda (ε-clausura) para un conjunto o frozenset de estados."""
        actuales = set(estados) if isinstance(estados, (set, frozenset)) else {estados}
        sonda = list(actuales)
        
        while sonda:
            est = sonda.pop()
            # Buscar transiciones lambda (representadas como '' o 'lambda')
            for simbolo in ['', 'lambda', 'ε']:
                key = (est, simbolo)
                if key in self.transiciones:
                    for destino in self.transiciones[key]:
                        if destino not in actuales:
                            actuales.add(destino)
                            sonda.append(destino)
        return frozenset(actuales)

    def simular_cadena(self, cadena):
        """ Simula una cadena y retorna (aceptada: bool, traza: list) """
        traza = []
        
        if self.tipo in ['AFD', 'AFND']:
            estado_actual = self.inicial
            traza.append({estado_actual})
            
            for simbolo in cadena:
                if simbolo not in self.alfabeto:
                    return False, traza # Símbolo fuera del alfabeto
                
                key = (estado_actual, simbolo)
                if key in self.transiciones:
                    destinos = self.transiciones[key]
                    # Si es AFND, tomamos el primer destino o manejamos conjunto
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
            current_states = self._clausura_lambda(self.inicial)
            traza.append(set(current_states))
            
            for simbolo in cadena:
                if simbolo not in self.alfabeto:
                    return False, traza
                
                siguientes = set()
                for est in current_states:
                    key = (est, simbolo)
                    if key in self.transiciones:
                        for destino in self.transiciones[key]:
                            siguientes.update(self._clausura_lambda(destino))
                
                current_states = frozenset(siguientes)
                traza.append(set(current_states))
                
            aceptada = any(est in self.aceptacion for est in current_states)
            return aceptada, traza

        return False, traza