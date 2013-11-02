
package mafiafirsttry;

enum Alignment {
    Town, Mafia, NeutralEvil, Neutral, Cult;
}

public abstract class Role {
    
    int vests = 0;

    int number;
    
   Alignment align;
   
   String roleName  = "Does not have role name yet.";
   
   Boolean healed = false;
   
   Boolean jailed = false;
    
    Boolean abilityNight;
    
    Boolean abilityAvail;
    
    Boolean immune=false;
    
    String sheriffMess = "Does not have sheriff Message yet.";
    
    String investMess = "Does not have investigator Message yet.";
    
    Boolean isAlive = true;
    
    String LW = "Insert Last Will here.";
    
    public void useAbility(int target) {
        
    }
    
    public void setLW(String setLW) {
        LW = setLW;
    }
    
    public String getLW() {
        System.out.println(LW);
        return LW;
    }
}
