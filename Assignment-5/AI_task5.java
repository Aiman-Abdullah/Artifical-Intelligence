package ai;

import java.io.BufferedReader;
import java.io.FileReader;

public class AI_task5 {

    public static BufferedReader reader;

    public static void main(String[] args) throws Exception {
        reader = new BufferedReader(new FileReader("C:\\Users\\Programmer\\Desktop\\AI Fall2020\\HomeWorks\\Assignment5_1001472426\\training_data.txt"));
        String x;
        double total = 0;
        double T_n_oN = 0;
        double N_no_T = 0;
        double falseT_n_N = 0;
        double true_Tgiven_B = 0;
        double true_F_given_TnN = 0;
        double true_F_given_T = 0;
        double true_F_given_N = 0;
        double true_F_no_T_nn = 0;
        double a;
        double b;
        double c;
        double d;
        double T_b = 0;
        double T_V = 0;
        double T_f = 0;
        double T_N = 0;

        while ((x = reader.readLine()) != null) {
            x = x.replaceAll("\\s", "");

            total = total + 1;
            a = Character.getNumericValue(x.charAt(0)) * 1.0;
            b = Character.getNumericValue(x.charAt(1)) * 1.0;
            c = Character.getNumericValue(x.charAt(2)) * 1.0;
            d = Character.getNumericValue(x.charAt(3)) * 1.0;
            
            if (a == 1) {

                T_b = T_b + 1;
            }

            if (b == 1) {
                T_V = T_V + 1;

                if (a == 1) {
                    true_Tgiven_B = true_Tgiven_B + 1;
                }
            }

            if (c == 1) {
                T_f = T_f + 1;
            }

            if ((b == 1) && (c == 1)) {
                T_N = T_N + 1;
            } else if (c == 1) {
                N_no_T = N_no_T + 1;
            } else if (b == 1) {
                T_n_oN = T_n_oN + 1;
            } else {
                falseT_n_N = falseT_n_N + 1;
            }
            if (d == 1) {

                if ((b == 1) && (c == 1)) {
                    true_F_given_TnN = true_F_given_TnN + 1;
                } else if (c == 1) {
                    true_F_given_N = true_F_given_N + 1;
                } else if (b == 1) {
                    true_F_given_T = true_F_given_T + 1;
                } else {
                    true_F_no_T_nn = true_F_no_T_nn + 1;
                }
            }
        }

        System.out.println("\n p(B) = " + (T_b / total));
        System.out.println("\n p(G|B) for B = true  = " + (true_Tgiven_B / T_b));
        System.out.println("\n p(G|B) for B = false = " + ((T_V - true_Tgiven_B) / (total - T_b)));
        System.out.println("\n p(O) = " + (T_f / total));
        System.out.println("\n p(F|G,O) for G = true & O = true       = " + (true_F_given_TnN / T_N));
        System.out.println("\n p(F|G,O) for G = false & O = true      = " + (true_F_given_N / N_no_T));
        System.out.println("\n p(F|G,O) for G = true & O = false      = " + (true_F_given_T / T_n_oN));
        System.out.println("\n p(F|G,O) for G = false & O = false     = " + (true_F_no_T_nn / falseT_n_N));
    }

}
