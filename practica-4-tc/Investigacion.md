**INVESTIGACIÓN: AUTÓMATAS FINITOS,\
LENGUAJES REGULARES Y EXPRESIONES REGULARES**

*Etapa 6 -- Teoría de la Computación*

# Introducción

En esta investigación se explican algunos conceptos importantes de la teoría de la computación. El propósito es entender qué son los lenguajes regulares, las expresiones regulares y los autómatas finitos, así como conocer cómo se relacionan y para qué pueden servir. También se explican algunas reglas algebraicas que utiliza el proyecto del simulador.

# 1. Lenguaje regular y expresión regular {#lenguaje-regular-y-expresión-regular}

Un lenguaje es un conjunto de cadenas formadas con símbolos de un alfabeto. Por ejemplo, si el alfabeto es {0, 1}, algunas cadenas posibles son 0, 1, 01 y 110. Un lenguaje regular es un conjunto de cadenas que puede ser reconocido por un autómata finito. También puede describirse mediante una expresión regular (Sipser, 2012; Hopcroft et al., 2007).

Una expresión regular es una forma de escribir un patrón para representar las cadenas que pertenecen a un lenguaje. En la notación usada en este proyecto, el símbolo + representa la unión, la concatenación se escribe juntando expresiones, y el asterisco \* significa que una parte puede repetirse cero o más veces.

Ejemplo: (0+1)\* representa todas las cadenas que se pueden formar usando ceros y unos, incluida la cadena vacía.

En el proyecto también se utilizan λ o ε para representar la cadena vacía, y ∅ para representar el lenguaje que no contiene ninguna cadena. Es importante no confundir la cadena vacía con el lenguaje vacío.

# 2. Jerarquía de Chomsky {#jerarquía-de-chomsky}

La jerarquía de Chomsky organiza distintos tipos de gramáticas y lenguajes en cuatro niveles. Cada nivel puede describir lenguajes con estructuras más generales que el nivel anterior (Hopcroft et al., 2007; Sipser, 2012).

**Tipo 3: regulares.** Son los más sencillos de esta clasificación. Se pueden reconocer con autómatas finitos y describir con expresiones regulares.

**Tipo 2: libres de contexto.** Permiten describir estructuras con reglas que tienen un solo símbolo no terminal a la izquierda. Se relacionan con los autómatas de pila.

**Tipo 1: sensibles al contexto.** Sus reglas pueden depender del contexto en el que aparecen los símbolos. Son más generales que las gramáticas libres de contexto.

**Tipo 0: no restringidas.** Es el nivel más general. Se relaciona con las máquinas de Turing y puede describir lenguajes reconocibles por ellas.

En resumen, los lenguajes regulares son una parte de una clasificación más amplia. No todos los lenguajes pueden reconocerse con un autómata finito.

# 3. Teorema de Kleene {#teorema-de-kleene}

El teorema de Kleene explica que las expresiones regulares y los autómatas finitos tienen el mismo poder para representar lenguajes regulares. Esto significa que un lenguaje descrito con una expresión regular puede reconocerse mediante un autómata finito, y que el lenguaje reconocido por un autómata finito puede describirse con una expresión regular (Sipser, 2012; Hopcroft et al., 2007).

## De expresión regular a autómata

Primero se construye un autómata no determinista con transiciones λ a partir de la expresión regular. Después se pueden quitar las transiciones λ, convertir el autómata en determinista y minimizarlo. En el proyecto, este recorrido se muestra como: ER → AFN-λ → AFN → AFD → AFD mínimo.

## De autómata a expresión regular

También se puede hacer el camino contrario: partir de un autómata finito y obtener una expresión regular que describa el mismo lenguaje. El proyecto realiza esta conversión mediante el método de eliminación de estados, conocido en el código como método Rij.

# 4. Reglas algebraicas de las expresiones regulares {#reglas-algebraicas-de-las-expresiones-regulares}

Las expresiones regulares tienen reglas que permiten simplificarlas sin cambiar las cadenas que representan. En el proyecto se aplican las siguientes reglas:

| Regla                            | Forma simplificada              |
|----------------------------------|---------------------------------|
| Unión con lenguaje vacío         | R + ∅ = R                       |
| Unión repetida                   | R + R = R                       |
| Concatenación con cadena vacía   | Rε = εR = R                     |
| Concatenación con lenguaje vacío | R∅ = ∅R = ∅                     |
| Cerradura del lenguaje vacío     | ∅\* = ε                         |
| Cerradura de la cadena vacía     | ε\* = ε                         |
| Cerradura repetida               | (R\*)\* = R\*                   |
| Dos cerraduras seguidas          | R\*R\* = R\*                    |
| Absorción                        | R + RR\* = R\* y R + R\*R = R\* |

La letra R representa cualquier expresión regular. Estas reglas ayudan a que las expresiones sean más cortas y fáciles de leer. El simplificador del proyecto aplica estas equivalencias, pero no pretende transformar todas las expresiones posibles en una única forma final.

# 5. Diferencia entre expresiones regulares teóricas y las de programación {#diferencia-entre-expresiones-regulares-teóricas-y-las-de-programación}

En teoría de la computación, las expresiones regulares se estudian como una manera formal de describir lenguajes regulares. Normalmente se usan operaciones básicas como unión, concatenación y cerradura.

En los lenguajes de programación, las expresiones regulares se usan como herramientas para buscar, revisar o sustituir texto. Dependiendo del lenguaje o biblioteca, pueden incluir funciones adicionales, por ejemplo clases de caracteres, repeticiones con límites, grupos y referencias a grupos. Por eso, las expresiones regulares de programación pueden tener más recursos que las expresiones regulares básicas de la teoría (Python Software Foundation, s. f.).

Por ejemplo, en Python se usa el módulo re para trabajar con patrones de texto. Su documentación explica símbolos como \[0-9\], \\d, \*, +, ? y los grupos entre paréntesis. Estas herramientas son útiles en programas, pero no todas forman parte de la notación básica que acepta el analizador de este proyecto.

# 6. Lema de bombeo para lenguajes regulares {#lema-de-bombeo-para-lenguajes-regulares}

El lema de bombeo es una propiedad que deben cumplir todos los lenguajes regulares. En palabras sencillas, si un lenguaje es regular, existe un número límite a partir del cual cualquier cadena suficientemente larga del lenguaje puede dividirse en tres partes: x, y y z. La parte y no puede estar vacía, y se puede repetir cero, una o varias veces; al hacerlo, la cadena sigue perteneciendo al lenguaje (Sipser, 2012).

La forma general se escribe: w = xyz, y las cadenas x yⁱ z pertenecen al lenguaje para i = 0, 1, 2, \...

Este lema se utiliza principalmente para demostrar que ciertos lenguajes no son regulares. Si se supone que un lenguaje es regular y se demuestra que no puede cumplir la propiedad del lema, entonces se concluye que no es regular. El lema no sirve por sí solo para demostrar que un lenguaje sí es regular.

Ejemplo conocido: el lenguaje {0ⁿ1ⁿ \| n ≥ 0}, que contiene la misma cantidad de ceros al inicio que de unos al final, no es regular. Un autómata finito no tiene memoria ilimitada para contar una cantidad arbitraria de ceros y después comprobar que aparece exactamente la misma cantidad de unos.

# 7. Cinco aplicaciones de los autómatas y las expresiones regulares {#cinco-aplicaciones-de-los-autómatas-y-las-expresiones-regulares}

**Validación de datos.** Permiten revisar si un dato tiene una forma esperada. Por ejemplo, comprobar que un campo de teléfono contenga cierta cantidad de dígitos. La expresión regular revisa el formato; otras reglas pueden ser necesarias para confirmar que el dato sea real.

**Búsqueda de texto.** Se pueden usar patrones para encontrar palabras, números o formatos dentro de un documento. Por ejemplo, localizar todas las partes de un texto que tengan una secuencia de dígitos.

**Análisis léxico.** Los compiladores utilizan patrones para reconocer elementos del código, como identificadores, números y palabras reservadas. Estos elementos se conocen como tokens.

**Revisión de fechas.** Un patrón puede comprobar que una fecha tenga una estructura como día/mes/año. Sin embargo, para saber si el día existe en ese mes y año, el programa debe hacer una validación adicional.

**Reconocimiento de secuencias.** Un autómata puede revisar si una secuencia de símbolos cumple ciertas reglas. Por ejemplo, identificar si una entrada está formada únicamente por 0 y 1 y si termina en 01.

Estas aplicaciones muestran que los autómatas y las expresiones regulares no son solamente conceptos matemáticos: también sirven para revisar información y reconocer patrones en programas (Hopcroft et al., 2007; Python Software Foundation, s. f.).

# 8. Relación de la investigación con el proyecto {#relación-de-la-investigación-con-el-proyecto}

El simulador desarrollado en esta práctica reúne varios de los conceptos explicados. Permite escribir una expresión regular y convertirla en diferentes tipos de autómatas; también permite minimizar un AFD, obtener una expresión regular mediante eliminación de estados, simplificar expresiones y comparar dos AFD para revisar si reconocen el mismo lenguaje.

Además, incluye ejemplos de validación de teléfono, fecha y contraseña. Estos ejemplos muestran cómo se pueden aplicar los patrones a datos cotidianos. La herramienta JFLAP también permite crear y convertir autómatas, expresiones regulares y otros modelos de lenguajes formales, por lo que puede utilizarse como apoyo para revisar los resultados (Rodger & Finley, s. f.).

# Conclusión

Los lenguajes regulares, las expresiones regulares y los autómatas finitos están relacionados porque representan y reconocen el mismo tipo de lenguajes. El teorema de Kleene explica esta relación. Las reglas algebraicas ayudan a simplificar expresiones, mientras que el lema de bombeo permite demostrar que algunos lenguajes no son regulares. Finalmente, estos temas tienen aplicaciones en la validación de datos, búsqueda de texto y análisis de código. El proyecto permite observar varias de estas operaciones de manera práctica.

# Referencias

Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2007). Introduction to automata theory, languages, and computation (3rd ed.). Pearson.

Python Software Foundation. (s. f.). re --- Operaciones con expresiones regulares. Python 3.11. https://docs.python.org/es/3.11/library/re.html

Rodger, S. H., & Finley, T. W. (s. f.). What is JFLAP? JFLAP. https://www.jflap.org/whatis.html

Sipser, M. (2012). Introduction to the theory of computation (3rd ed.). Cengage Learning.

Nota sobre las fuentes: se utilizaron libros de texto universitarios y documentación oficial de Python y JFLAP. No se usaron blogs, Wikipedia ni páginas de apuntes. Las referencias se presentan en formato APA séptima edición.
