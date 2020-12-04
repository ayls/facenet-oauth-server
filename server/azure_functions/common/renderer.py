def renderTemplate(htmlFilename: str, variables: dict) -> str:
  htmlFile = open(htmlFilename, 'r')
  htmlContent = htmlFile.read()
  htmlFile.close()

  for varName, varValue in variables.items():
    varPlaceholder = '{{{{{id}}}}}'.format(id=varName)
    htmlContent = htmlContent.replace(varPlaceholder, varValue)

  return htmlContent