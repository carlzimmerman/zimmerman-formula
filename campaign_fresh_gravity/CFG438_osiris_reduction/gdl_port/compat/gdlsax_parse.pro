;-----------------------------------------------------------------------------
; GDLSAX_PARSE, obj, filename
;
; GDL PORT SHIM (infrastructure only, no reduction logic).
; GDL 1.0.1's native IDLffXMLSAX::ParseFile delivers only ONE attribute per
; element to StartElement (AttNames/AttValues arrays have the right length
; but only element 0 is filled), and does not bind SELF in StartDocument /
; EndDocument.  The OSIRIS DRP backbone reads its config file and the DRF
; XML through those callbacks, so this routine walks the XML text and calls
; obj->StartElement, URI, Local, qName, AttNames, AttValues exactly as IDL's
; SAX parser would (EndElement is called too if the object defines it).
; Comments, <?...?> and <!...> declarations are skipped.  Standard XML
; entities in attribute values are decoded.
;-----------------------------------------------------------------------------
FUNCTION gdlsax_decode, s
  r = s
  ents = [['&lt;','<'],['&gt;','>'],['&quot;','"'],['&apos;',"'"],['&amp;','&']]
  FOR k = 0, (SIZE(ents,/DIM))[1]-1 DO BEGIN
    WHILE (p = STRPOS(r, ents[0,k])) GE 0 DO $
      r = STRMID(r,0,p) + ents[1,k] + STRMID(r, p+STRLEN(ents[0,k]))
  ENDFOR
  RETURN, r
END

PRO gdlsax_parse, obj, filename
  OPENR, lun, filename, /GET_LUN
  line = ''
  txt = ''
  WHILE ~EOF(lun) DO BEGIN
    READF, lun, line
    txt = txt + line + ' '
  ENDWHILE
  FREE_LUN, lun
  b = BYTE(txt)
  n = N_ELEMENTS(b)
  i = 0L
  q1 = (BYTE('"'))[0] & q2 = (BYTE("'"))[0]
  lt_ = (BYTE('<'))[0] & gt_ = (BYTE('>'))[0]
  WHILE i LT n DO BEGIN
    IF b[i] NE lt_ THEN BEGIN
      i = i + 1
      CONTINUE
    ENDIF
    ; comment
    IF STRMID(txt, i, 4) EQ '<!--' THEN BEGIN
      e = STRPOS(txt, '-->', i+4)
      IF e LT 0 THEN MESSAGE, 'Unterminated comment in ' + filename
      i = e + 3
      CONTINUE
    ENDIF
    ; find the end of the tag, respecting quotes
    j = i + 1
    inq = 0B
    WHILE j LT n DO BEGIN
      c = b[j]
      IF inq EQ 0B THEN BEGIN
        IF c EQ q1 OR c EQ q2 THEN inq = c ELSE IF c EQ gt_ THEN BREAK
      ENDIF ELSE IF c EQ inq THEN inq = 0B
      j = j + 1
    ENDWHILE
    IF j GE n THEN MESSAGE, 'Unterminated tag in ' + filename
    tag = STRTRIM(STRING(b[i+1:j-1]), 2)
    i = j + 1
    first = STRMID(tag, 0, 1)
    IF first EQ '?' OR first EQ '!' THEN CONTINUE
    IF first EQ '/' THEN BEGIN
      qName = STRTRIM(STRMID(tag, 1), 2)
      IF OBJ_HASMETHOD(obj, 'EndElement') THEN obj->EndElement, '', '', qName
      CONTINUE
    ENDIF
    selfclose = 0
    IF STRMID(tag, STRLEN(tag)-1, 1) EQ '/' THEN BEGIN
      selfclose = 1
      tag = STRTRIM(STRMID(tag, 0, STRLEN(tag)-1), 2)
    ENDIF
    sp = STREGEX(tag, '[[:space:]]')
    IF sp LT 0 THEN BEGIN
      qName = tag
      rest = ''
    ENDIF ELSE BEGIN
      qName = STRMID(tag, 0, sp)
      rest = STRMID(tag, sp)
    ENDELSE
    names = [''] & vals = [''] & na = 0
    WHILE 1 DO BEGIN
      pos = STREGEX(rest, '([A-Za-z_][A-Za-z0-9_.:-]*)[[:space:]]*=[[:space:]]*("[^"]*"|' + "'[^']*')", $
                    /SUBEXPR, LENGTH=len)
      IF pos[0] LT 0 THEN BREAK
      nm = STRMID(rest, pos[1], len[1])
      v  = STRMID(rest, pos[2]+1, len[2]-2)
      IF na EQ 0 THEN BEGIN
        names = [nm] & vals = [gdlsax_decode(v)]
      ENDIF ELSE BEGIN
        names = [names, nm] & vals = [vals, gdlsax_decode(v)]
      ENDELSE
      na = na + 1
      rest = STRMID(rest, pos[0] + len[0])
    ENDWHILE
    IF na GT 0 THEN obj->StartElement, '', '', qName, names, vals $
    ELSE obj->StartElement, '', '', qName
    IF selfclose AND OBJ_HASMETHOD(obj, 'EndElement') THEN obj->EndElement, '', '', qName
  ENDWHILE
END
