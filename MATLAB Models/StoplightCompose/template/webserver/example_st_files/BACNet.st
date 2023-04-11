FUNCTION_BLOCK Simulator
  VAR_OUTPUT
    Out : REAL;
  END_VAR
  VAR_INPUT
    MinVal : REAL;
    MaxVal : REAL;
    PeriodSeconds : INT;
  END_VAR
  VAR
    TON0 : TON;
    seconds : INT;
    BaseVal : REAL;
    VarVal : REAL;
  END_VAR

  (* pseudo-random variations *)
  TON0(IN := TRUE, PT := T#3120s);
  IF TON0.Q THEN
    TON0(IN := FALSE);
  END_IF;
  seconds := TIME_TO_INT(TON0.ET);

  BaseVal := (MaxVal + MinVal)/2.0;
  VarVal  := (MaxVal-MinVal)*INT_TO_REAL((seconds MOD PeriodSeconds) - (PeriodSeconds/2))/INT_TO_REAL(PeriodSeconds);

  Out :=  BaseVal + VarVal;
END_FUNCTION_BLOCK

PROGRAM program0
  VAR
    EnergyCounter AT %MD0.2.0 : REAL;
    Temperature AT %ID0.0.0 : REAL;
    Humidity AT %ID0.0.1 : REAL;
  END_VAR
  VAR
    TempSimulation : Simulator;
    HumiditySimulation : Simulator;
  END_VAR
  VAR
    TemperatureSetPoint AT %QD0.1.0 : REAL;
    ControlDisable AT %QX0.4.2 : BOOL;
    Heater AT %IX0.3.0 : BOOL;
    Cooler AT %IX0.3.1 : BOOL;
  END_VAR
  VAR
    ADD3_OUT : REAL;
    GT16_OUT : BOOL;
    AND19_OUT : BOOL;
    LT17_OUT : BOOL;
    AND24_OUT : BOOL;
  END_VAR

  ADD3_OUT := ADD(EnergyCounter, 0.00131);
  EnergyCounter := ADD3_OUT;
  TempSimulation(MinVal := 18.0, MaxVal := 30.0, PeriodSeconds := 120);
  Temperature := TempSimulation.Out;
  HumiditySimulation(MinVal := 55.0, MaxVal := 78.0, PeriodSeconds := 58);
  Humidity := HumiditySimulation.Out;
  GT16_OUT := GT(Temperature, TemperatureSetPoint);
  AND19_OUT := AND(NOT(ControlDisable), GT16_OUT);
  Cooler := AND19_OUT;
  LT17_OUT := LT(Temperature, TemperatureSetPoint);
  AND24_OUT := AND(NOT(ControlDisable), LT17_OUT);
  Heater := AND24_OUT;
END_PROGRAM


CONFIGURATION config

  RESOURCE resource1 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : program0;
  END_RESOURCE
END_CONFIGURATION
