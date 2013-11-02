

package mafiafirsttry;

import java.lang.Thread;

public class ThreadDay extends Thread{
    
    public void run(int cycle) {
        System.out.println("Day " + cycle + " has started");
         try {Thread.sleep(2000);} 
         catch(InterruptedException ex) {Thread.currentThread().interrupt();}
         
         
    }
    
}
