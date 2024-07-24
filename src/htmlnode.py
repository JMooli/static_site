
class HTMLnode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLnode:(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"
 
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        for key, value in self.props.items():
            result = ''.join(key + '= "' + value + '"')
        return result