# cofi-code-challenge
En este repositorio se plantea mi solución al code challenge de Cofi.

En store/store.py está toda la lógica de la aplicación.

El carro almacena las cantidades de cada objeto que se han añadido, y a la hora de obtener el total, calcula los descuentos pertinentes.
Éstos se añaden a un segundo carro _dummy_ como un objeto más, y se eliminan los objetos que conforman el descuento.

Por ejemplo, si tenemos los siguientes items en el carro principal:
- VOUCHER: 3
- TSHIRT: 1
- MUG: 1

Nuestro carro _dummy_ quedará de la siguiente manera:
- SWAG: 1
- VOUCHER2x1: 1

Y con ésto se calcula el total.

Los descuentos en mi solución se aplican en el siguiente orden (Los descuentos se pueden aplicar más de una vez si se cumplen los requisitos):
1. Descuento "SWAG" al tener 1 de cada objeto.
2. Descuento "VOUCHER2x1" al tener 2 "VOUCHER"
3. Descuento "BULK_TSHIRT" al tener 3 ó más "TSHIRT"

En tests.py se encuentran los tests unitarios de la aplicación, con distintos descuentos mezclados, y cantidades de objetos
