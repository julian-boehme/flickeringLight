# flickering light.py

import maya.cmds as cmds
import random

def flickeringLight(pObject, pStartTime, pEndTime, pMinIntervalOff, pMaxIntervalOff, pMinIntervalOn, pMaxIntervalOn, pAttribute, pLowLightMinValue, pLowLightMaxValue, pFullLightValue, pProbabilityForSubsequentLows):
    """Creates a randomly flickering light. The values alternate between random values and the max values.
    pObject : A string representing the name of the object whose attributes are to be manipulated
    pStartTime : The start time for setting keyframes in frames
    pEndTime : The end time for setting keyframes in frames
    pMinIntervalOff : The minimum interval size in frames to the next keyframe in an "off" interval (low light, not full light intensity)
    pMaxIntervalOff : The maximum interval size in frames to the next keyframe in an "off" interval (low light, not full light intensity)
    pMinIntervalOn : The minimu interval size in frames to the next keyframe in an "on" interval (light has full intensity)
    pMaxIntervalOn : The minimu interval size in frames to the next keyframe in an "on" interval (light has full intensity)
    pAttributes : the attribute to be manipulated
    pLowLightMinValues : the minimum float value for the attribute
                        This is the minimum value, that can occur in a low light situation
    pLowLightMaxValues : The maximum float value for the attribute
                        This is the maximum value, that can occur in a low light situation
    pFullLightValue : The value for the maximum intensity of the light.
    pProbabilityForSubsequentLows : The propability, that after a low light situation, directly another low light situation follows
                                    The higher the value, the higher the possibility for subsequent low light situations, without returning to full light inbetween
                                    e.g. 1, if after every low there shall be full light value
                                    e.g. 2: the possibility, that the light returns to full value after a low is 50%
                                            There is a 50% chance, that another low will follow the last low
    """
    useFullLightValue = True;            #the light should alternate between the max value (on) and a random value
    keyTime = pStartTime;
    currentValue = 0.0;
    #keyInterval: if the interval between the last and the current keyframe is only 1, don't set a hold-key! That would be unnecessary and delete the most recent set keyframe
    keyInterval = 0;
    while(keyTime < pEndTime):
        #for i in range(len(pAttributes)):
        ## Set hold-keyframe, but start after the first keyframe (meaning: keytime > pStartTime):
        if(keyTime > pStartTime and keyInterval>1):    
          cmds.setKeyframe(pObject, attribute = pAttribute, time = keyTime-1.0, value = currentValue); 
        ##
        
        
        if(useFullLightValue):
            highAfterLowValue = random.randint(1, pProbabilityForSubsequentLows);
            if(highAfterLowValue == 1):
                currentValue = pFullLightValue;
                cmds.setKeyframe(pObject, attribute = pAttribute, time = keyTime, value = currentValue)
                useFullLightValue = False;
                keyInterval = random.randint(pMinIntervalOn, pMaxIntervalOn);
                keyTime = keyTime + keyInterval;
            else:
                useFullLightValue = False;
        else:
            currentValue = random.uniform(pLowLightMinValue, pLowLightMaxValue);
            cmds.setKeyframe(pObject, attribute = pAttribute, time = keyTime, value = currentValue)
            useFullLightValue = True;
            keyInterval = random.randint(pMinIntervalOff, pMaxIntervalOff);
            keyTime = keyTime + keyInterval;
        #cmds.setKeyframe(pObject, attribute = pAttribute, time = keyTime, value = currentValue)
        #useFullLightValue = not useFullLightValue;
        ##
        #if(useFullLightValue):
            #keyTime = keyTime + random.randint(pMinIntervalOn, pMaxIntervalOn);
        #else:
            #keyTime = keyTime + random.randint(pMinIntervalOff, pMaxIntervalOff);
        ##
            
        


flickeringLight("flickering_area_lightShape", 0, 3260, 1, 4, 5, 48, "intensity", 0.0, 5.0, 10.0, 3);
flickeringLight("flickering_area_lightShape", 3260, 3415, 1, 4, 1, 3, "intensity", 0.0, 5.0, 10.0, 1);


