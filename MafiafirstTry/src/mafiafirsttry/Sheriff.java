


package mafiafirsttry;

import java.lang.Boolean;

public class Sheriff extends Role {
    
 
    public Sheriff() {

        align = Alignment.Town;
        abilityNight = true;
        sheriffMess = "This person is not suspicious";
       roleName = "Sheriff";
       investMess = "Your target is an excellent judge of character; they are likely a "
               + "Sheriff, but could also be a Blackmailer or even an Executioner.";
       
    }
    
    public void useAbility(int target) {
        System.out.println((GameController.roleList.get(target).sheriffMess) + "\n");
    }
    
    void printWelcome() {
         System.out.println("You are a sheriff. Your alignment is " + 
                 "Town"
                 + ". You are only with the town. Kill all cult, mafia and neutral evil to win the game.");
    }
    
    

}
