import { useState, useContext, useEffect } from 'react'
import { AppContext } from '../../context/AppContext'

import styles from './styles.module.css'
import Markdown from 'react-markdown'

// const changedMade =
//   '1. Nullifying Pointers After Freeing:\nAfter freeing memory (free(a) and free(d)), the pointers are set to NULL. This ensures that subsequent operations (like double freeing or UAF) will not occur, as attempting to free or use a NULL pointer is safe.\n\n2. Conditional Freeing:\nBefore calling free(d) the second time, the code checks if d is NULL. This prevents a double-free vulnerability.\n\n3. Check for Validity Before Use:\nBefore using the pointer a, the code checks if it is not NULL. This prevents use-after-free vulnerabilities.\n\n4. Error Handling:\nThe malloc calls are checked for success. If the memory allocation fails, an error message is displayed, and the program exits gracefully. This avoids potential issues with using unallocated memory.\n\nThese changes ensure the code is robust against double-free and use-after-free vulnerabilities, and they follow safe programming practices.'

// const code =
//   '#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n\tint *a = malloc(0x50);\n\tif (a == NULL) {\n\t\tperror("Memory allocation failed");\n\t\treturn 1;\n\t}\n\t\n\tfree(a);\n\ta = NULL;  // Nullify pointer after free\n\t\n\tint *d = malloc(0x50);\n\tif (d == NULL) {\n\t\tperror("Memory allocation failed");\n\t\treturn 1;\n\t}\n\t\n\tfree(d);\n\td = NULL;  // Nullify pointer after free\n\t\n\t// Avoid double free\n\tif (d != NULL) {\n\t\tfree(d);\n\t}\n\t\n\t// Avoid use-after-free\n\tif (a != NULL) {\n\t\tprintf("%p\n", a);\n\t} else {\n\t\tprintf("Pointer a has been freed and nullified\n");\n\t}\n\t\n\treturn 0;\n}'

export default function PatchSuggestion() {
  const { appState } = useContext(AppContext)

  const [code, setCode] = useState("")
  const [changesMade, setChangesMade] = useState("")

  useEffect(() => {
    if (appState.patchResult !== undefined) {
      setCode(appState.patchResult.code)
      setChangesMade(appState.patchResult.description)
    }
  }, [])

  return (
    <div className={styles.cards}>
      <div className={styles.card}>
        <h2>Description</h2>
        <div style={{ color: 'white', paddingLeft: '12px' }}>
          <Markdown>{changesMade}</Markdown>
        </div>
      </div>
      <div className={styles.card}>
        <h2>Patched Code</h2>
        <textarea
          className={styles.whiteTextArea}
          readOnly={true}
          value={code}
          onChange={e => setCode(e.target.value)}
        ></textarea>
      </div>
    </div>
  )
}
