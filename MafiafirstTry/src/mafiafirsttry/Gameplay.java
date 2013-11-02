/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package mafiafirsttry;

import static mafiafirsttry.GameController.roleList;


public class Gameplay {
    

        
public static void night1() {
        //Survivor
        int target = 5;
        if (roleList.get(5).isAlive == true)roleList.get(5).useAbility(target);
        // DOCTOR
        target = 0;
        if (roleList.get(3).isAlive == true)roleList.get(3).useAbility(target);
        //SK
        target = 0;
        if (roleList.get(1).isAlive == true) roleList.get(1).useAbility(target);
        //GF
        target = 1;
        if (roleList.get(4).isAlive == true)roleList.get(4).useAbility(target);
        //SHERIFF
        target = 1;
        if (roleList.get(0).isAlive == true) roleList.get(0).useAbility(target);
        //INVEST
        target = 0;
        if (roleList.get(2).isAlive == true)roleList.get(2).useAbility(target);
        
        
        
        }
        
        
public static void night2() {
      
        //Survivor
        int target = 5;
        if (roleList.get(5).isAlive == true)roleList.get(5).useAbility(target);
        // DOCTOR
        target = 5;
        if (roleList.get(3).isAlive == true)roleList.get(3).useAbility(target);
        //SK
        target = 2;
        if (roleList.get(1).isAlive == true) roleList.get(1).useAbility(target);
        //GF
        target = 5;
        if (roleList.get(4).isAlive == true)roleList.get(4).useAbility(target);
        //SHERIFF
        target = 2;
        if (roleList.get(0).isAlive == true) roleList.get(0).useAbility(target);
        //INVEST
        target = 1;
        if (roleList.get(2).isAlive == true)roleList.get(2).useAbility(target);
        }
        
        
public static void night3() {
        //Survivor
        int target = 5;
        if (roleList.get(5).isAlive == true)roleList.get(5).useAbility(target);
        // DOCTOR
        target = 1;
        if (roleList.get(3).isAlive == true)roleList.get(3).useAbility(target);
        //SK
        target = 0;
        if (roleList.get(1).isAlive == true) roleList.get(1).useAbility(target);
        //GF
        target = 5;
        if (roleList.get(4).isAlive == true)roleList.get(4).useAbility(target);
        //SHERIFF
        target = 3;
        if (roleList.get(0).isAlive == true) roleList.get(0).useAbility(target);
        //INVEST
        target = 2;
        if (roleList.get(2).isAlive == true)roleList.get(2).useAbility(target);
        }

public static void night4() {
        //Survivor
        int target = 5;
        if (roleList.get(5).isAlive == true) roleList.get(5).useAbility(target);
        // DOCTOR
        target = 1;
        if (roleList.get(3).isAlive == true)roleList.get(3).useAbility(target);
        //SK
        target = 5;
        if (roleList.get(1).isAlive == true) roleList.get(1).useAbility(target);
        //GF
        target = 1;
        if (roleList.get(4).isAlive == true)roleList.get(4).useAbility(target);
        //SHERIFF
        target = 1;
        if (roleList.get(0).isAlive == true) roleList.get(0).useAbility(target);
        //INVEST
        target = 0;
        if (roleList.get(2).isAlive == true)roleList.get(2).useAbility(target);
        roleList.remove(1);
        
        
        
}

public static void night5() {
     //Survivor
        int target = 5;
        if (roleList.get(5).isAlive == true)roleList.get(5).useAbility(target);
        // DOCTOR
        target = 0;
        if (roleList.get(3).isAlive == true)roleList.get(3).useAbility(target);
        //SK
        target = 3;
        if (roleList.get(1).isAlive == true) roleList.get(1).useAbility(target);
        //GF
        target = 1;
        if (roleList.get(4).isAlive == true)roleList.get(4).useAbility(target);
        //SHERIFF
        target = 1;
        if (roleList.get(0).isAlive == true) roleList.get(0).useAbility(target);
        //INVEST
        target = 0;
        if (roleList.get(2).isAlive == true)roleList.get(2).useAbility(target);
}

public static void night6() {
     //Survivor
        int target = 5;
        if (roleList.get(5).isAlive == true)roleList.get(5).useAbility(target);
        // DOCTOR
        target = 0;
        if (roleList.get(3).isAlive == true)roleList.get(3).useAbility(target);
        //SK
        target = 4;
        if (roleList.get(1).isAlive == true) roleList.get(1).useAbility(target);
        //GF
        target = 1;
        if (roleList.get(4).isAlive == true)roleList.get(4).useAbility(target);
        //SHERIFF
        target = 1;
        if (roleList.get(0).isAlive == true) roleList.get(0).useAbility(target);
        //INVEST
        target = 0;
        if (roleList.get(2).isAlive == true)roleList.get(2).useAbility(target);
}
}
