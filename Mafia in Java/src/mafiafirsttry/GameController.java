
package mafiafirsttry;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.lang.Thread;



public class GameController {

    int cycle = 0;
    
    
    
    List<User> userList;
    static List<Role> roleList;
    
    public GameController() {
        roleList = new ArrayList<>();
        userList = new ArrayList<>();
        createRoleList();
        
        
    }
    
   
    
    public void daynight() {
        int victory=0;
        while (victory == 0) {
        cycle++;
        //              REMOVE jailed and healed from doctors, every morning
        for (int j = 0;j<roleList.size();j++) {
            roleList.get(j).healed = false;
            roleList.get(j).jailed = false;
        }
        System.out.println("Day " + cycle + " has begun.");
        
            victory = victoryCheck();
            
            if (victory!=0){
                
                
             /*   try {
    
} catch(InterruptedException ex) {
    Thread.currentThread().interrupt();
}*/
                
                //0 continue, 1 MM, 2 Arso, 3 SK, 4 Mafia, 5 Town, 6 Cult, 7 none 
                
                System.out.println("The game has reached a conclusion."); 
                if (victory == 3) System.out.println("The serial killer won the game.");
                if (victory == 4) System.out.println("The mafia won the game.");
                if (victory == 5) System.out.println("The town won the game.");
                Boolean survwin = survivorwin(); 
           if (survwin) System.out.println("The survivor lived to see the end. He also won the game.");
           System.out.println("People alive: ");
           for (int i=0;i<roleList.size();i++) {
               if (roleList.get(i).isAlive == true) System.out.println("player " + (i+1) + ", " + roleList.get(i).roleName + " was alive.");
           }
                 
                break;
            }
        
        //Wait 2 seconds
        try {
    Thread.sleep(2000);
} catch(InterruptedException ex) {
    Thread.currentThread().interrupt();
}
      
        System.out.println("Night " + cycle + " has begun.\n");
       
        for (int i=0;i<roleList.size(); i++) {
           if (roleList.get(i).abilityNight)  
         roleList.get(i).abilityAvail = true;
        }
        
        if (cycle == 1) Gameplay.night1();
        if (cycle == 2) Gameplay.night2();
        if (cycle == 3) Gameplay.night3();
        if (cycle == 4) Gameplay.night4();
        if (cycle == 5) Gameplay.night5();
        if (cycle == 6) Gameplay.night6();
        
        
        }
    }
    
    public int victoryCheck() {
        //kør igennem metoder for hver alignment
         //0 continue, 1 MM, 2 Arso, 3 SK, 4 Mafia, 5 Town, 6 Cult, 7 none  
        Boolean winner = skwin();
        if (winner == true) {return 3;}
        winner = mafiawin();
        if (winner == true) {
           Boolean survwin = survivorwin(); 
           if (survwin) return 14;
           return 4;
        }
        winner = townwin();
        if (winner == true) return 5;
        
        
        
        
        return 0;
        
    }
    
    public Boolean skwin() {
        int enemiesAlive=0;
        for (int i = 0;i<roleList.size();i++) {
            if (roleList.get(i).align == Alignment.Town && roleList.get(i).isAlive==true) enemiesAlive++;
            else if (roleList.get(i).align == Alignment.Mafia && roleList.get(i).isAlive==true) enemiesAlive++;
            else if (roleList.get(i).align == Alignment.Cult && roleList.get(i).isAlive==true) enemiesAlive++;
            else if (roleList.get(i).align == Alignment.Neutral && roleList.get(i).isAlive==true) enemiesAlive++;
        }
        if (enemiesAlive > 1) return false;
            return true;
    }
    
    public Boolean mafiawin() {
        int enemiesAlive=0, evilAlive=0;
        for (int i = 0;i<roleList.size();i++) {
            if (roleList.get(i).align == Alignment.Town && roleList.get(i).isAlive==true) enemiesAlive++;
            else if (roleList.get(i).align == Alignment.NeutralEvil && roleList.get(i).isAlive==true) {enemiesAlive++; evilAlive++;}
            else if (roleList.get(i).align == Alignment.Cult && roleList.get(i).isAlive==true) enemiesAlive++;
            else if (roleList.get(i).align == Alignment.Neutral && roleList.get(i).isAlive==true) enemiesAlive++;
        }
        if (enemiesAlive<2) {
            if (evilAlive < 1) return true;
        }
            return false; 
    }
    
    public Boolean townwin() {
     int enemiesAlive=0;
        for (int i = 0;i<roleList.size();i++) {
                if (roleList.get(i).align == Alignment.NeutralEvil && roleList.get(i).isAlive==true) enemiesAlive++;
            else if (roleList.get(i).align == Alignment.Mafia && roleList.get(i).isAlive==true) enemiesAlive++;
            else if (roleList.get(i).align == Alignment.Cult && roleList.get(i).isAlive==true) enemiesAlive++;
        }
        if (enemiesAlive>0) return false;
            return true;
    }
    
    public Boolean survivorwin() {
        for (int i = 0;i<roleList.size();i++) {
                if (roleList.get(i).roleName == "Survivor" && roleList.get(i).isAlive==true) return true;
    }
        return false;
    }
     
    
    public void createRoleList() {
   
    System.out.println("Choose which roles you want in the game.");
    // Add 1 sheriff (input name from user??)
      Role sheriff = new Sheriff();
    // Add 1 SK
        Role serialkiller = new SerialKiller();    
         // Add 1 invest
        Role invest = new Investigator(); 
        // Add 1 doc
        Role doctor = new Doctor(); 
         // Add 1 GF
        Role godfather = new Godfather(); 
         // Add 1 Survivor
        Role survivor = new Survivor(); 
    roleList.add(sheriff);
    roleList.add(serialkiller);
    roleList.add(invest);
    roleList.add(doctor);
    roleList.add(godfather);
    roleList.add(survivor);
    //Collections.shuffle(roleList);
    
    for (int i=0; i<roleList.size(); i++) {
    
    System.out.println("Player " + (i+1) + " is: " + roleList.get(i).roleName);
    }
    
    
   
    
    }
}
