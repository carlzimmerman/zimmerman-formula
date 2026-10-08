;-----------------------------------------------------------------------------
; GDL PORT SHIM (infrastructure only, no reduction logic).
; GDL 1.0.1 has no IDLffXMLDOMDocument.  assembcube_000.pro uses it only to
; read $OSIRIS_DRP_DATA_PATH/calibrations.xml and pick the wavelength-solution
; file by date.  This is a minimal read-only DOM implementing exactly the calls
; used there: Document::GetFirstChild, Node::GetElementsByTagName,
; NodeList::GetLength/Item, Node::GetAttribute, Node::GetFirstChild (text
; node), Node::GetNodeValue.
;-----------------------------------------------------------------------------
FUNCTION gdlDomNode::Init, name, ISTEXT=istext, VALUE=value
  Self.name = name
  Self.istext = KEYWORD_SET(istext)
  IF N_ELEMENTS(value) GT 0 THEN Self.value = value
  Self.attn = PTR_NEW(/ALLOCATE_HEAP)
  Self.attv = PTR_NEW(/ALLOCATE_HEAP)
  Self.kids = PTR_NEW(/ALLOCATE_HEAP)
  RETURN, 1
END
PRO gdlDomNode::Cleanup
END
PRO gdlDomNode::AddAttr, n, v
  IF N_ELEMENTS(*Self.attn) EQ 0 THEN BEGIN
    *Self.attn = [n] & *Self.attv = [v]
  ENDIF ELSE BEGIN
    *Self.attn = [*Self.attn, n] & *Self.attv = [*Self.attv, v]
  ENDELSE
END
PRO gdlDomNode::AddKid, o
  IF N_ELEMENTS(*Self.kids) EQ 0 THEN *Self.kids = [o] ELSE *Self.kids = [*Self.kids, o]
END
FUNCTION gdlDomNode::GetName
  RETURN, Self.name
END
FUNCTION gdlDomNode::GetKids
  IF N_ELEMENTS(*Self.kids) EQ 0 THEN RETURN, OBJ_NEW()
  RETURN, *Self.kids
END
FUNCTION gdlDomNode::GetAttribute, n
  IF N_ELEMENTS(*Self.attn) EQ 0 THEN RETURN, ''
  w = WHERE(*Self.attn EQ n, c)
  IF c EQ 0 THEN RETURN, ''
  RETURN, (*Self.attv)[w[0]]
END
FUNCTION gdlDomNode::GetFirstChild
  IF N_ELEMENTS(*Self.kids) EQ 0 THEN RETURN, OBJ_NEW()
  RETURN, (*Self.kids)[0]
END
FUNCTION gdlDomNode::GetNodeValue
  RETURN, Self.value
END
PRO gdlDomNode::Collect, name, list
  IF N_ELEMENTS(*Self.kids) EQ 0 THEN RETURN
  FOR k = 0, N_ELEMENTS(*Self.kids)-1 DO BEGIN
    o = (*Self.kids)[k]
    IF o->GetName() EQ name THEN list->Append, o
    o->Collect, name, list
  ENDFOR
END
FUNCTION gdlDomNode::GetElementsByTagName, name
  list = OBJ_NEW('gdlDomNodeList')
  Self->Collect, name, list
  RETURN, list
END
PRO gdlDomNode__define
  void = {gdlDomNode, name:'', istext:0, value:'', attn:PTR_NEW(), attv:PTR_NEW(), kids:PTR_NEW()}
END

FUNCTION gdlDomNodeList::Init
  Self.items = PTR_NEW(/ALLOCATE_HEAP)
  RETURN, 1
END
PRO gdlDomNodeList::Cleanup
END
PRO gdlDomNodeList::Append, o
  IF N_ELEMENTS(*Self.items) EQ 0 THEN *Self.items = [o] ELSE *Self.items = [*Self.items, o]
END
FUNCTION gdlDomNodeList::GetLength
  RETURN, N_ELEMENTS(*Self.items)
END
FUNCTION gdlDomNodeList::Item, i
  RETURN, (*Self.items)[i]
END
PRO gdlDomNodeList__define
  void = {gdlDomNodeList, items:PTR_NEW()}
END

FUNCTION IDLffXMLDOMDocument::Init, FILENAME=filename
  Self.root = OBJ_NEW('gdlDomNode', '#document')
  IF N_ELEMENTS(filename) GT 0 THEN Self->Load, filename
  RETURN, 1
END
PRO IDLffXMLDOMDocument::Cleanup
END
FUNCTION IDLffXMLDOMDocument::GetFirstChild
  RETURN, Self.root->GetFirstChild()
END
PRO IDLffXMLDOMDocument::Load, filename
  OPENR, lun, filename, /GET_LUN
  line = '' & txt = ''
  WHILE ~EOF(lun) DO BEGIN
    READF, lun, line
    txt = txt + line + ' '
  ENDWHILE
  FREE_LUN, lun
  b = BYTE(txt) & n = N_ELEMENTS(b)
  q1 = (BYTE('"'))[0] & q2 = (BYTE("'"))[0]
  lt_ = (BYTE('<'))[0] & gt_ = (BYTE('>'))[0]
  stack = [Self.root]
  i = 0L
  WHILE i LT n DO BEGIN
    IF b[i] NE lt_ THEN BEGIN
      e = STRPOS(txt, '<', i)
      IF e LT 0 THEN e = n
      t = STRTRIM(STRMID(txt, i, e-i), 2)
      IF t NE '' THEN stack[N_ELEMENTS(stack)-1]->AddKid, OBJ_NEW('gdlDomNode', '#text', /ISTEXT, VALUE=t)
      i = e
      CONTINUE
    ENDIF
    IF STRMID(txt, i, 4) EQ '<!--' THEN BEGIN
      e = STRPOS(txt, '-->', i+4)
      IF e LT 0 THEN MESSAGE, 'Unterminated comment in ' + filename
      i = e + 3
      CONTINUE
    ENDIF
    j = i + 1 & inq = 0B
    WHILE j LT n DO BEGIN
      c = b[j]
      IF inq EQ 0B THEN BEGIN
        IF c EQ q1 OR c EQ q2 THEN inq = c ELSE IF c EQ gt_ THEN BREAK
      ENDIF ELSE IF c EQ inq THEN inq = 0B
      j = j + 1
    ENDWHILE
    tag = STRTRIM(STRING(b[i+1:j-1]), 2)
    i = j + 1
    first = STRMID(tag, 0, 1)
    IF first EQ '?' OR first EQ '!' THEN CONTINUE
    IF first EQ '/' THEN BEGIN
      IF N_ELEMENTS(stack) GT 1 THEN stack = stack[0:N_ELEMENTS(stack)-2]
      CONTINUE
    ENDIF
    selfclose = 0
    IF STRMID(tag, STRLEN(tag)-1, 1) EQ '/' THEN BEGIN
      selfclose = 1
      tag = STRTRIM(STRMID(tag, 0, STRLEN(tag)-1), 2)
    ENDIF
    sp = STREGEX(tag, '[[:space:]]')
    IF sp LT 0 THEN BEGIN
      qName = tag & rest = ''
    ENDIF ELSE BEGIN
      qName = STRMID(tag, 0, sp) & rest = STRMID(tag, sp)
    ENDELSE
    node = OBJ_NEW('gdlDomNode', qName)
    WHILE 1 DO BEGIN
      pos = STREGEX(rest, '([A-Za-z_][A-Za-z0-9_.:-]*)[[:space:]]*=[[:space:]]*("[^"]*"|' + "'[^']*')", $
                    /SUBEXPR, LENGTH=len)
      IF pos[0] LT 0 THEN BREAK
      node->AddAttr, STRMID(rest, pos[1], len[1]), gdlsax_decode(STRMID(rest, pos[2]+1, len[2]-2))
      rest = STRMID(rest, pos[0] + len[0])
    ENDWHILE
    stack[N_ELEMENTS(stack)-1]->AddKid, node
    IF ~selfclose THEN stack = [stack, node]
  ENDWHILE
END
PRO IDLffXMLDOMDocument__define
  void = {IDLffXMLDOMDocument, root:OBJ_NEW()}
END
