.[].createdAt |= { "$date": (. | sub(" "; "T")) }
| .[].updatedAt |= { "$date": (. | sub(" "; "T")) }
