#Obilasci nam sluze da pristupimo svakom cvoru stabla, bez da i jedan preskocimo (radi pretrage, izmene, ubacivanja novog elem...)
#kod opsteg, n-arnog stabla mozemo dodati cvor bilo gde (na root, bilo koji cvor...)
#dodavanje elementa na prosledjenu vrednost O(n), na referencu O(1)

from queue import Queue

class TreeNode(object):

    #implementacija atributa je dinamicka u py i mogu se dodati u bilo kom trenutku, u pozadini
    #kljucevi se cuvaju u recnicima (naziv:vrednost) - za male objekte nepotrebno trosenje memorije
    #Drugi nacin implementacije atributa - __slots__ - deklaracija atributa unapred

    __slots__ = 'parent', 'children', 'data' #najavljujemo da ce klasa imati tri navedena atributa, nema recnika, mnogo manje memorije trosimo

    def __init__(self, data, parent = None, children = None):
        if children is None:
            self.children = []
        self.parent = parent
        self.data = data

    def num_children(self):
        return len(self.children)

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return len(self.children) == 0

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def remove_child(self, child_node):
        self.children.remove(child_node)

    def __str__(self):
        return str(self.data)

class Tree(object):

    def __init__(self, root = None):
        self.root = root

    def is_empty(self):
        return self.root is None

    def nodes(self):
        pass

    def replace(self, old_node, new_node):
        parent = old_node.parent
        new_node.parent = parent
        parent.remove_child(old_node)
        parent.add_child(new_node)
        for child in old_node.children:
            new_node.add_child(child)

    def depth(self, node):
        if node.is_root():
            return 0
        else:
            return 1 + self.depth(node.parent)

    def _height(self, node):
        if node.is_leaf():
            return 0
        else:
            return 1 + max(self._height(c) for c in node.children)

    def height(self):
        return self._height(self.root)

    def preorder(self, root):
        #prvo cvor pa deca
        print(root)
        for child in root.children:
            self.preorder(child)

    def postorder(self, root):
        #prvo deca pa cvor
        for child in root.children:
            self.postorder(child)
        print(root)

    def breadth_first(self):
        #preko Queua

        wait_list = Queue()
        wait_list.enqueue(self.root)

        while not wait_list.is_empty():
            first = wait_list.dequeue()
            print(first, self.depth(first))
            for child in first.children:
                wait_list.enqueue(child)

    def print_tree(self):
        print("\nGame tree:")
        self.breadth_first()

#da bi graf bio stablo - veze u stablu zapravo nisu neusmerene (imaju jasno odredjen smer (ko je kome dete/roditelj)),
#nacin crtanja stabla po niovima nam omogucava da zanemarimo da su strelice usmerene
#kod grafa postoje izolovani cvorovi, kod stabala ne (osim ako to nije jedini cvor stabla)
#ne moze da postoji vise korena, ne postoje cirkularne veze kod stabala

if __name__ == '__main__':
    a = TreeNode("a")
    b = TreeNode("b")
    c = TreeNode("c")
    d = TreeNode("d")

    a.add_child(b)
    a.add_child(c)
    c.add_child(d)

    t = Tree(a)
    t.preorder(t.root)
    print()
    t.postorder(t.root)
    print()
    t.breadth_first()

    print()
    print(t.depth(d))

    e = TreeNode("e")
    d.add_child(e)

    print()
    print(t.height())
