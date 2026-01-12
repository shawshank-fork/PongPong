from pyamaze import maze, agent, textLabel, COLOR

def DFS(m,start=None):
    if start is None:
        start = (m.rows,m.cols)
    explored=[start]
    frontier=[start]
    dfsPath={}
    dSearch=[]
    while len(frontier)>0:
        curCell = frontier.pop()
        dSearch.append(curCell)
        if curCell == m._goal:
            break
        poss = 0

        for d in 'ESNW' :
            if m.maze_map[curCell][d] == True:
                if d == 'E':
                    child = (curCell[0], curCell[1] + 1)
                if d == 'W':
                    child = (curCell[0], curCell[1] - 1)
                if d == 'N':
                    child = (curCell[0] - 1, curCell[1])
                if d == 'S':
                    child = (curCell[0] + 1, curCell[1])
                if child in explored:
                    continue
                poss += 1

                explored.append(child)
                frontier.append(child)
                dfsPath[child] = curCell
        if poss>1:
            m.markCells.append(curCell)
    fwdPath = {}
    cell = m._goal
    while cell!= start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]
    return dSearch, dfsPath, fwdPath

if __name__=='__main__':
    m = maze(10,10)
    m.CreateMaze(2,4)

    dSearch,dfsPath,fwdPath = DFS(m,(5,1))

    a = agent(m,5,1,goal = (2,4), footprints = True, shape = 'square', color = COLOR.green)
    b = agent(m,2,4,goal = (5,1), footprints = True, filled = True)
    c = agent(m,5,1, footprints = True, color = COLOR.yellow)
    m.tracePath({a:dSearch}, showMarked = True)
    m.tracePath({b:dfsPath})
    m.tracePath({c:fwdPath})
    m.run()