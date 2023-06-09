PROGRAM test_main
  VAR
    PLC_OUT AT %QW0.0.2.8193.0 : INT;
    PLC_IN AT %IW0.0.2.8192.0 : INT;
  END_VAR
  VAR
    ADD4_OUT : INT;
  END_VAR

  ADD4_OUT := ADD(1, PLC_IN);
  PLC_OUT := ADD4_OUT;
END_PROGRAM


CONFIGURATION conf

  RESOURCE res ON PLC
    TASK tache(INTERVAL := t#50ms,PRIORITY := 0);
    PROGRAM toto WITH tache : test_main;
  END_RESOURCE
END_CONFIGURATION
