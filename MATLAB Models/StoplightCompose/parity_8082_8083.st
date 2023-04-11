PROGRAM Stoplight
  VAR
    lamp_red AT %QX0.0 : BOOL;
    lamp_yel AT %QX0.1 : BOOL;
    lamp_gre AT %QX0.2 : BOOL;
    adjacent_red AT %IX0.0 : BOOL;
    adjacent_yel AT %IX0.1 : BOOL;
    adjacent_gre AT %IX0.2 : BOOL;
  END_VAR
  
  VAR
    count : INT;
    again : BOOL;
  END_VAR
  
  IF adjacent_yel THEN
    again := True;
  END_IF;
  
  count := count + 1;
  IF adjacent_red AND again THEN
    lamp_gre := True;
    lamp_red := False;
    again := False;
    count := 0;
  ELSIF (count > 2) AND (count < 4) THEN
    lamp_gre := False;
    lamp_yel := True;
  ELSIF count > 3 THEN
    lamp_yel := False;
    lamp_red := True;
  END_IF;
  
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#1000ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : Stoplight;
  END_RESOURCE
END_CONFIGURATION
