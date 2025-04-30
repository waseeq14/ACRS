import React, { createContext, useState } from 'react'

export const AppContext = createContext()

export const AppProvider = ({ children }) => {
  const [appState, setAppState] = useState({
    // =======================
    // Mockup Data for Testing
    // =======================
    //
    // kleeResult: {
    //   analysis:
    //     '**Markdown**\n*Italic*\n`Code`\n## Heading 2\n> Blockquote\n**Bold**',
    //   code: 'Some code'
    // },
    // advancedKleeResult: {
    //   analysis:
    //     '**Markdown**\n*Italic*\n`Code`\n## Heading 2\n> Blockquote\n**Bold**',
    //   segments: ['Code 1', 'Code 2', 'Code 3', 'Code 4']
    // },
    // fuzzerResult: {
    //   analysis:
    //     '**Markdown**\n*Italic*\n`Code`\n## Heading 2\n> Blockquote\n**Bold**',
    //   code: 'Code',
    //   seeds: 'Seeds'
    // },
    // rulesResult: [
    //   {
    //     snippet: 'Snippet',
    //     ai_analysis:
    //       '**Markdown**\n*Italic*\n`Code`\n## Heading 2\n> Blockquote\n**Bold**'
    //   },
    //   {
    //     snippet: 'Snippet',
    //     ai_analysis:
    //       '**Markdown**\n*Italic*\n`Code`\n## Heading 2\n> Blockquote\n**Bold**'
    //   },
    //   {
    //     snippet: 'Snippet',
    //     ai_analysis:
    //       '**Markdown**\n*Italic*\n`Code`\n## Heading 2\n> Blockquote\n**Bold**'
    //   },
    //   {
    //     snippet: 'Snippet',
    //     ai_analysis:
    //       '**Markdown**\n*Italic*\n`Code`\n## Heading 2\n> Blockquote\n**Bold**'
    //   }
    // ]
    //
    // pentest: {},
    // pentestExploit: {},
    // pentestPatch: {}
    //
    // user: {}
    //
    // projects: {}
    // pentestProjects: {}
  })

  return (
    <AppContext.Provider value={{ appState, setAppState }}>
      {children}
    </AppContext.Provider>
  )
}
