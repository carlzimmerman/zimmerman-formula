; GDL compatibility shim for the IDL builtin BIN_DATE (not in GDL 1.0.1).
; Returns [year, month, day, hour, minute, second] from a SYSTIME()-format string.
FUNCTION BIN_DATE, ascii_time
  IF N_ELEMENTS(ascii_time) EQ 0 THEN ascii_time = SYSTIME()
  months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
  p = STRSPLIT(STRTRIM(ascii_time,2), ' ', /EXTRACT)
  mon = (WHERE(months EQ STRUPCASE(p[1])))[0] + 1
  t = STRSPLIT(p[3], ':', /EXTRACT)
  RETURN, LONG([LONG(p[4]), mon, LONG(p[2]), LONG(t[0]), LONG(t[1]), LONG(t[2])])
END
