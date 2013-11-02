


package mafiafirsttry;

import java.lang.Boolean;
import java.util.Random;

public class SerialKiller extends Role{
    
    
    String[] deathMess = {"He was found with mutiple stab wounds.","His body was severely battered with many broken bones. "
            + "He had multiple stab wounds.","He had bruises and some bone fractures in addition to his multiple stab wounds."};
    
   
    public SerialKiller() {
        immune = true;
        roleName = "Serial killer";
        align = Alignment.NeutralEvil;
        abilityNight = true;
        sheriffMess = "Your target is a serial killer!";
        investMess = "Your target owns weapons and spends his nights trying to kill people; "
                + "therefore, they are a Mafioso or a Serial Killer, but could also be just a Vigilante.";
    }
    
    public void useAbility(int target) {
        //check om død allerede
        if (GameController.roleList.get(target).isAlive == true) {
            
            if (GameController.roleList.get(target).healed == false) {
            
        //                  SUCCESFULD KILL!!
        if (GameController.roleList.get(target).immune == false) {
        
        //add besked når dagen starter/natten slutter
      System.out.println("Player " + ((GameController.roleList.indexOf(GameController.roleList.get(target))+1) + " has been killed"));
      //random en SK dødsbesked
      Random rand = new Random();
        int choice = rand.nextInt(3);
        System.out.println(deathMess[choice]);
      System.out.println(("His role was: " + GameController.roleList.get(target).roleName) + "\n");
        GameController.roleList.get(target).isAlive = false;
        }
        
        //                  UNSUCCESFULL KILL!!!
        if (GameController.roleList.get(target).immune == true || GameController.roleList.get(target).jailed == true ) {
            System.out.println("Target was not able to be killed.");
        }
        }
            else System.out.println("Target was not able to be killed.");
                }
        else System.out.println("Target was already dead.");
       
        
    
    }

    
    public void printWelcome() {
         System.out.println("You are a serial killer. Your alignment is " + 
                 "Neutral"
                 + ". You are only with yourself. Kill all town, cult and mafia to win the game.");
    }
    
    


}