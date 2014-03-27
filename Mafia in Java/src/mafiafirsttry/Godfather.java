


package mafiafirsttry;


import java.util.Random;

public class Godfather extends Role{
    
    
    String[] deathMess = {"He was shot at close range.","There were signs of struggle. He/she was shot at close range."
            + "His body had bruises and minor fractures. He was also riddled with bullets at close range.",
            "There were signs of struggle. His body was battered and had multiple bone fractures. He was shot at close range."};
    
   
    public Godfather() {
        immune = true;
        roleName = "Godfather";
        align = Alignment.Mafia;
        abilityNight = true;
        sheriffMess = "This person is not suspicious";
        investMess = "You discover nothing of importance, suggesting that your target is as unsuspicious as a "
               + "Citizen, Crier, Survivor, or a bedridden Amnesiac.";
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
         System.out.println("You are the godfather. Your alignment is " + 
                 "Mafia"
                 + ". Kill all town, cult and neutral evil to win the game.");
    }
    
    


}