PROGRAM test_main
  VAR
    outvar AT %QW0.0.8192.0 : INT;
    invar AT %IW0.0.8193.0 : INT;
  END_VAR
  VAR
    ADD4_OUT : INT;
  END_VAR

  ADD4_OUT := ADD(1, invar);
  outvar := ADD4_OUT;
END_PROGRAM


CONFIGURATION conf

  RESOURCE res ON PLC
    TASK tache(INTERVAL := T#10ms,PRIORITY := 0);
    PROGRAM toto WITH tache : test_main;
  END_RESOURCE
END_CONFIGURATION
