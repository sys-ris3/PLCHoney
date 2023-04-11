PROGRAM Stoplight
  VAR
    lamp_red AT %QX0.0 : BOOL;
    lamp_yel AT %QX0.1 : BOOL;
    lamp_gre AT %QX0.2 : BOOL;
  END_VAR
  
  VAR
    run : BOOL;
    red : BOOL;
    yel : BOOL;
    gre : BOOL;
    count : INT;
  END_VAR
  
  run := True;
  count := count + 1;
  
  IF ((red = gre) AND (red = yel)) THEN
    red := True;
  END_IF;
  
  IF (red AND run) THEN
    IF count > 5 THEN
      lamp_gre := True;
      gre := True;
      lamp_red := False;
      red := False;
      run := False;
      count := 0;
    END_IF;
  END_IF;
  
  IF (yel AND run) THEN
    IF count > 2 THEN
      lamp_yel := False;
      yel := False;
      lamp_red := True;
      red := True;
      run := False;
      count := 0;
    END_IF;
  END_IF;
  
  IF (gre AND run) THEN
    IF count > 3 THEN
      lamp_gre := False;
      gre := False;
      lamp_yel := True;
      yel := True;
      run := False;
      count := 0;
    END_IF;
  END_IF;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#1000ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : Stoplight;
  END_RESOURCE
END_CONFIGURATION
