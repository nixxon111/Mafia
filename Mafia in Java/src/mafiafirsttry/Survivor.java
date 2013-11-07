


package mafiafirsttry;

import java.lang.Boolean;

public class Survivor extends Role {
    
 
    public Survivor() {
        vests = 3;
        align = Alignment.Neutral;
        abilityNight = true;
        sheriffMess = "This person is not suspicious";
       roleName = "Survivor";
       investMess = "You discover nothing of importance, suggesting that your target is as unsuspicious as a "
               + "Citizen, Crier, Survivor, or a bedridden Amnesiac.";
       
    }
    
    public void useAbility(int target) {
        if ( vests>0) {
            GameController.roleList.get(target).healed = true;
        vests--;
        }
    }
    
    void printWelcome() {
         System.out.println("You are a sheriff. Your alignment is " + 
                 "Town"
                 + ". You are only with the town. Lynch all cult, mafia and neutral evil to win the game.");
    }
    
    

}
