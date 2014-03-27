


package mafiafirsttry;

import java.lang.Boolean;

public class Investigator extends Role {
    
 
    public Investigator() {

        align = Alignment.Town;
        abilityNight = true;
        sheriffMess = "This person is not suspicious";
       roleName = "Investigator";
       investMess = "Your target seems skilled at reading people and searching homes, "
               + "leading you to believe that they are an Investigator or a Consigliere, or possibly a Disguiser.";
       
    }
    
    public void useAbility(int target) {
        System.out.println((GameController.roleList.get(target).investMess) + "\n");
    }
    
    void printWelcome() {
         System.out.println("You are a sheriff. Your alignment is " + 
                 "Town"
                 + ". You are only with the town. Kill all cult, mafia and neutral evil to win the game.");
    }
    
    

}
