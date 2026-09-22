**Estado del arte**

**[Articulo 1=\> Applications of Deterministic Finite Automata]{.mark}**

La principal diferencia entre un AFD y la maquina de Mealy es que esta es un transductor de estados finitos. esta produce una **cadena de salida** a medida que consume símbolos de entrada. Su función de salida asocia una emisión a cada transición entre estados. A diferencia de el AFD que su salida es de naturaleza binaria (la cadena de entrada se *acepta* o se *rechaza* dependiendo de si el estado final pertenece al conjunto de estados de aceptación.

**¿Por qué Apache Lucene requiere una Máquina de Mealy para el autocompletado?**

Porque el motor de búsqueda de Apache Lucene no solo responde un prefijo si no que necesita devolver datos adicionales, este puede emitir diferentes salidas como frecuencias de búsqueda o pesos.

**Consecuencia de declarar vacío el conjunto de estados de aceptación**

Al definir el conjunto de estados finales como el conjunto vacio el lenguaje aceptado por el automata es el lenguaje vacio en pocas palabras ninguna cadena de entrada es aceptada.

Una afirmación del documento que convendría verificar es cuando dice que el uso de las maquinas de Mealy en apache lucene reducen el consumo de ram en comparación con otras estructuras de datos. Yo considero que esto se tendría que verificar bien bien porque en algunos casos el tiempo de ejecución puede ser algo engañoso.

**[Articulo 2 =\> Melanoma detection in dermoscopic images using a cellular automata classifier.]{.mark}**

**Autómata Finito (AF) vs Autómata Celular (AC)**

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th><strong>Semejanzas</strong></th>
<th><strong>Diferencias</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Ambos son modelos computacionales discretos en tiempo y estado.</td>
<td>Estructura espacial, Un autómata finito es una única unidad central de control que cambia de estado según una cadena de entrada secuencial. Y un autómata celular consiste en una malla D-dimensional de celdas idénticas que evoluciona de manera espacial y sincrónicamente en paralelo.</td>
</tr>
<tr>
<td>Utilizan un conjunto finito de estados y una función o regla de transición de estados determinista.</td>
<td><p>En el AC</p>
<p>El estado es valor discreto que toma una celda en un instante de tiempo t.</p>
<p>Vecindario son el conjunto finito de celdas adyacentes o cercanas a una celda dada.</p></td>
</tr>
</tbody>
</table>

El problema que abordan es el diagnóstico preclínico y detección de cancer de la piel a partir de imágenes dentro de sistemas CAD. Y eligen el AC porque estos destacan en el análisis por su análisis espacial, capacidad de procesamiento. Tambien por el tipo de imágenes.

Resultados

Lograron un modelo que supera a otros modelos tradicionales en la clasificación de imágenes dermatológicas.

Metricas utilizadas

Exactitud =\>97.8%

Sensibilidad =\>94.4%

Especificidad =\> 98.7%

[Articulo 3 =\> ON COMPUTABLE NUMBERS, WITH AN APPLICATION TO]{.mark}

[THE ENTSCHEIDUNGSPROBLEM]{.mark}

Se demuestra el Entscheidungsproblem bueno la maquina de Turing o como el la menciona a-machine, que es un modelo abstracto que esta compuesto por una cinta infinita dividida en muchas celdas, la cual cuenta con un lector-escritor además de un conjunto de estados internos. En si lo que demuestra turin es la imposibilidad de resolver mecánicamente el Entscheidungsproblem, se prueba que no existe ningún algoritmo ni serie de pasos o procedimientos para poder resolver este ejercicio.

La Tesis de Church-Turing =\>Toda función que pueda considerarse efectivamente computable por medios intuitivos u operacionalmente realizables por un ser humano siguiendo un conjunto finito de instrucciones simples, es computable por una Máquina de Turing (y equivalentemente, por el Cálculo Lambda de Alonzo Church).

Se le llama tesis y no teorema, porque no existe manera de demostrarlo formalmente con los axiomas, es un concepto muy abstracto que no se puede formalizar.

Qué dificultad encontró en su lectura=\> La primer barrera y la mas importante fue el idioma aunque si entendia masomenos que decía si en algunos momento se me dificultaba y al final por temas de tiempo traduje todo y lo lei en español, En cuanto a notación también fue muy muy complicado, fue muy desafiante.

[Articulo 4 =\> Finite State Automata on Multi-Word Units for Efficient Text-Mining]{.mark}^ ^

El artículo aborda la ineficiencia computacional y el alto consumo de memoria que sufren los sistemas tradicionales de minería de texto y Procesamiento de Lenguaje Natural al intentar extraer e identificar expresiones compuestas o unidades multipalabra en grandes volúmenes de datos no estructurados. En este Proponen el diseño de software el cual compila expresiones sintéticas dentro de un AFD que esta optimizado para el reconocimiento de patrones.

Se demuestran que el procesamiento de texto mediante el autómata compilado logra un tiempo de ejecución lineal O(n) en función de la longitud del texto, reduciendo drásticamente el tiempo de procesamiento y el espacio en memoria. Este articulo se relaciona explícitamente con los temas de Autómatas Finitos Deterministas (AFD), Expresiones Regulares y el Reconocimiento de Cadenas en Lenguajes Regulares. Este articulo nos sirve de ejemplo para ver como los conceptos abstractos vistos en clase se traducen en herramientas reales de software para optimizar procesos y disminuir el uso de recursos.

[Articulo 5 =\> Automated Runtime Verification of Security for E-Commerce Smart Contracts]{.mark}

Este articulo analiza el problema de la \"explosión de estados\" ocurre al convertir Autómatas Finitos No Deterministas (AFN) en Autómatas Finitos Deterministas (AFD) y la falta de métricas cuantitativas para medir el grado de no-determinismo en lenguajes regulares. El articulo desarrollan un marco de análisis teórico que evalúa el costo computacional (espacio en memoria versus tiempo de evaluación) de distintas variantes de autómatas finitos, proponiendo algoritmos para la determinización y minimización de estados. Obtienen resultados muy positivos, Nos permite evaluar cunado el uso de AFN es mejor o mas compacto que de AFD. Este articulo se relaciona con los temas de Autómatas Finitos No Deterministas (AFN), Equivalencia entre AFD y AFN y Minimización de Estados en Autómatas Finitos. Ayuda a profundiza la comprensión conceptual sobre el determinismo y no-determinismo.

<table style="width:92%;">
<colgroup>
<col style="width: 34%" />
<col style="width: 15%" />
<col style="width: 7%" />
<col style="width: 15%" />
<col style="width: 18%" />
</colgroup>
<thead>
<tr>
<th>Texto</th>
<th>Arbitro</th>
<th>Año</th>
<th>Modelo que usa</th>
<th>Campo de aplicacion</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong><mark>Applications of Deterministic Finite Automata</mark></strong></td>
<td>No</td>
<td>2013</td>
<td>Autómata Finito Determinista (AFD) / Máquina de Mealy</td>
<td>Docencia / Búsqueda y autocompletado de texto.</td>
</tr>
<tr>
<td><strong><mark>Melanoma detection in dermoscopic images using a cellular automata classifier.</mark></strong></td>
<td>Computers, MDPI</td>
<td>2022</td>
<td>Autómata Celular</td>
<td>Bioinformática / Diagnóstico médico por imágenes</td>
</tr>
<tr>
<td><p><mark>ON COMPUTABLE NUMBERS, WITH AN APPLICATION TO</mark></p>
<p><mark>THE ENTSCHEIDUNGSPROBLEM</mark></p></td>
<td>Proceedings of the LMS</td>
<td>1936</td>
<td>Máquina de Turing / Máquina Universal de Turing</td>
<td>Fundamentos de la Computación / Lógica Matemática</td>
</tr>
<tr>
<td><mark>Finite State Automata on Multi-Word Units for Efficient Text-Mining</mark><sup> </sup></td>
<td>Mathematics, MDPI</td>
<td>2024</td>
<td>Autómata Finito Determinista (AFD)</td>
<td>Procesamiento de Lenguaje Natural (PLN) / Minería de Texto</td>
</tr>
<tr>
<td><mark>Automated Runtime Verification of Security for E-Commerce Smart Contracts</mark></td>
<td>IEEE / Springer</td>
<td>2022</td>
<td>Autómata Finito / Verificación de Modelos (<em>Model Checking</em>)</td>
<td>Ciberseguridad / Verificación Formal de Software (Blockchain)</td>
</tr>
</tbody>
</table>

Referencias

Artículo 1. Gribkoff, E. (2013). Applications of deterministic finite automata \[Documento de curso, ECS 120\]. University of California, Davis. <https://www.cs.ucdavis.edu/~rogaway/classes/120/spring13/eric-dfa.pdf>

Artículo 2. Luna-Benoso, B., Martínez-Perales, J. C., Cortés-Galicia, J., Flores-Carapia, R., y Silva-García, V. M. (2022). Melanoma detection in dermoscopic images using a cellular automata classifier. Computers, 11(1), 8. <https://doi.org/10.3390/computers11010008>

Articulo 3, Turing, A. M. (1936). On computable numbers, with an application to the *Entscheidungsproblem*. *Proceedings of the London Mathematical Society*, *2*(42), 230--265. <https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf>

Articulo 4.  Silva, D. F., Castro, R. L., & Gomes, A. M. (2024). Finite state automata on multi-word units for efficient text-mining. *Mathematics*, *12*(4), Artículo 506. [https://www.mdpi.com/2227-7390/12/4/506](https://www.mdpi.com/2227-7390/12/4/506?utm_source=gemini)

Articulo 5. Zhang, M., & Liu, Y. (2022). Automated runtime verification of security for e-commerce smart contracts. *Journal of Theoretical and Applied Electronic Commerce Research*, 20(2), 73. [https://www.mdpi.com/0718-1876/20/2/73](https://www.mdpi.com/0718-1876/20/2/73?utm_source=gemini)
