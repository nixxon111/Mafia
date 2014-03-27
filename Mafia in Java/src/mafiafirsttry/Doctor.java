


package mafiafirsttry;

import java.lang.Boolean;

public class Doctor extends Role {
    
 
    public Doctor() {

        align = Alignment.Town;
        abilityNight = true;
        sheriffMess = "This person is not suspicious";
       roleName = "Doctor";
       investMess = "You discover a number of sharp tools and implements, suggesting that your target is "
               + "either a Doctor or a Witch, or if you're unlucky, a Witch Doctor.";
       
    }
    
    public void useAbility(int target) {
        GameController.roleList.get(target).healed = true;
    }
    
    void printWelcome() {
         System.out.println("You are a sheriff. Your alignment is " + 
                 "Town"
                 + ". You are only with the town. Lynch all cult, mafia and neutral evil to win the game.");
    }
    
    

}
