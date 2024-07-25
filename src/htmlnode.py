
class HTMLnode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __repr__(self) -> str:
        return f"HTMLnode:(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return ''.join(f' {key}="{value}"' for key, value in self.props.items())


class ParentNode(HTMLnode):
    def __init__(self, tag, children, props=None):
        if not children:
            raise ValueError("ParentNode must have children.")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if not self.children:
            raise ValueError("ParentNode must have children.")
        
        children_html = ''.join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"




class LeafNode(HTMLnode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value.")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        
        if self.tag is None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
