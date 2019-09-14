/*
 * Created on 04/09/2010
 * @author: Perez Ernesto Rafael
 */
package recrutisima;
//Puzzle.java
import java.math.BigInteger;
/*
 * Esto programa resuelve un computo de sumatoria de grandes números enteros 
 * aplicando aritmetica modular
 * 
 */

class Puzzle {

final static BigInteger M = new BigInteger("2017");


//metodo clasico para un calculo de sumatoria
private static BigInteger compute(long n) {
String s = "";
for (long i = 0; i < n; i++) {
s = s + n;
}
return new BigInteger(s.toString()).mod(M);
}

// metodo donde aplico aritmetica modular para grandes números
private static BigInteger compute2(long n) { 
String s = ""; 
//no paso el numero completo solo su resto
//String a = new BigInteger(n+"").mod(M)+"";
String a = String.valueOf( new BigInteger(String.valueOf(n)).mod(M));

// recorro hasta el resto
for (long i = 0; i < Integer.parseInt(a); i++) { 
s = s + a ; 
// aqui en vez de acumular n solo acumulo su modulo, los cual es equivalente 
//por la propiedad asociativad de aritmetica modular
s = String.valueOf(new BigInteger(s).mod(M)); 
System.out.println("i "+i+" s "+s);
} 
return new BigInteger(s.toString()).mod(M); 
}


public static void main(String args[]) {
//Long.valueOf (1),Long.valueOf (2)...
//for (long n : new long[] { 1L, 2L, 5L, 10L, 20L, 58184241583791680L }) {
 for (long n : new long[] { 1L, 2L, 5L, 10L, 20L, 58184241583791680L}) {
	 System.out.println("" + n + ": " + compute2(n));
	 //System.out.println("" + 5 + ": " + compute(5));
}
}

}