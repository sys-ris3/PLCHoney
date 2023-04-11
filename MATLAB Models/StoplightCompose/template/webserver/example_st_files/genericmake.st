PROGRAM program0
  VAR
    LocalVara : INT;
    LocalVarb : INT;
  END_VAR

  LocalVarb := LocalVara;
END_PROGRAM


CONFIGURATION config

  RESOURCE resource1 ON PLC
    TASK Tsk(INTERVAL := T#100ms,PRIORITY := 0);
    PROGRAM Inst WITH Tsk : program0;
  END_RESOURCE
END_CONFIGURATION
