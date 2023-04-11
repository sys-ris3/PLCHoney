PROGRAM Stoplight
  VAR
    lamp_red AT %QX0.0 : BOOL;
    lamp_yel AT %QX0.1 : BOOL;
    lamp_gre AT %QX0.2 : BOOL;
    adjacent_red AT %IX0.0 : BOOL;
    adjacent_yel AT %IX0.1 : BOOL;
    adjacent_gre AT %IX0.2 : BOOL;
  END_VAR
  
  IF adjacent_gre THEN
    lamp_gre := True;
    lamp_red := False;
  END_IF;
  
  IF adjacent_yel THEN
    lamp_yel := True;
    lamp_gre := False;
  END_IF;
  
  IF adjacent_red THEN
    lamp_red := True;
    lamp_yel := False;
  END_IF;
  
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#100ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : Stoplight;
  END_RESOURCE
END_CONFIGURATION
