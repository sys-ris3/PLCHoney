PROGRAM Stoplight
  VAR
    south_lamp_red AT %QX0.0 : BOOL;
    south_lamp_yel AT %QX0.1 : BOOL;
    south_lamp_gre AT %QX0.2 : BOOL;
    east_lamp_red AT %QX0.3 : BOOL;
    east_lamp_yel AT %QX0.4 : BOOL;
    east_lamp_gre AT %QX0.5 : BOOL;
    north_lamp_red AT %QX0.6 : BOOL;
    north_lamp_yel AT %QX0.7 : BOOL;
    north_lamp_gre AT %QX1.0 : BOOL;
    west_lamp_red AT %QX1.1 : BOOL;
    west_lamp_yel AT %QX1.2 : BOOL;
    west_lamp_gre AT %QX1.3 : BOOL;
  END_VAR
  
  VAR
    run : BOOL;
    count : INT;
    parity : BOOL;
    v_red : BOOL;
    v_yel : BOOL;
    v_gre : BOOL;
    h_red : BOOL;
    h_yel : BOOL;
    h_gre : BOOL;
  END_VAR
  
  run := True;
  count := count + 1;
  
  IF ((v_red AND h_gre) AND run) THEN
    IF count > 5 THEN
      h_gre := False;
      h_yel := True;
      run := False;
      count := 0;
    END_IF;
  END_IF;
  
  IF ((h_red AND v_gre) AND run) THEN
    IF count > 5 THEN
      v_gre := False;
      v_yel := True;
      run := False;
      count := 0;
    END_IF;
  END_IF;
  
  IF ((v_yel AND h_red) AND run) THEN
    v_yel := False;
    v_red := True;
    run := False;
  END_IF;
  
  IF ((h_yel AND v_red) AND run) THEN
    h_yel := False;
    h_red := True;
    run := False;
  END_IF;
  
  IF (v_red = h_red) THEN
    IF count > 3 THEN
      IF parity THEN
        v_red := True;
        h_gre := True;
        h_red := False;
        parity := False;
        count := 0;
      ELSE
        h_red := True;
        v_gre := True;
        v_red := False;
        parity := True;
        count := 0;
      END_IF;
    END_IF;
  END_IF;
  
  south_lamp_red := v_red;
  south_lamp_yel := v_yel;
  south_lamp_gre := v_gre;
  east_lamp_red := h_red;
  east_lamp_yel := h_yel;
  east_lamp_gre := h_gre;
  north_lamp_red := v_red;
  north_lamp_yel := v_yel;
  north_lamp_gre := v_gre;
  west_lamp_red := h_red;
  west_lamp_yel := h_yel;
  west_lamp_gre := h_gre;

END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#1000ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : Stoplight;
  END_RESOURCE
END_CONFIGURATION
