class Graph:
    def __init__(self):
        # 빈 그래프를 생성
        self.nodes = []
        self.links = []
    
    def add_node(self, node):
        # 이미 존재하는 node인 경우
        if node.index in [n.index for n in self.nodes]:
            print(f'Node {node.index} already exists')
            raise ValueError()
        else:
            self.nodes.append(node)
    
    def add_link(self, link):
        # 이미 존재하는 link인 경우
        if link.nodes in [l.nodes for l in self.links]:
            print(f'Link ({link.start} - {link.end}) already exists')
        else:
            # 설정된 node 내에서 만들어진 link인지 확인
            if (link.start in self.nodes) and (link.end in self.nodes):
                self.links.append(link)
            else:
                if (link.start not in self.nodes):
                    print(f'Node {link.start.index} does not exist')
                elif (link.end not in self.nodes):
                    print(f'Node {link.end.index} does not exist')
    
    def print_nodes(self):
        for n in self.nodes:
            print(n)
    
    def print_links(self):
        for l in self.links:
            print(l)
    
    def get_node(self, index):
        """
        index 숫자로부터 실제 node 객체를 가져오는 함수
        """
        if index not in [n.index for n in self.nodes]:
            raise ValueError(f'Node {index} not found')
        for n in self.nodes:
            if n.index == index:
                return n

    
    def get_link(self, start, end):
        """
        index나 node로 들어온 input으로부터 실제 link 객체를 가져오는 함수
        """
        # start와 end가 index 값을 뜻하는 int일 경우, Node 객체로 찾아서 변환
        if isinstance(start, int):
            start = self.get_node(start)
            
        if isinstance(end, int):
            end = self.get_node(end)
        
        # node 객체들로부터 매칭되는 link 찾기
        for l in self.links:
            if l.nodes == {start, end}:
                return l
        raise ValueError(f'Link ({start.index} - {end.index}) not found')