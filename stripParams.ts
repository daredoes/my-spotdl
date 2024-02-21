Bun.argv.slice(2).forEach((pLink: string) => {
  console.log(pLink.split("?")[0])
})