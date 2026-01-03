import ast

class CodeParser:
    def parse_text(self, content: str):
        """Parses code and splits it into logical chunks"""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return [content]
        
        chunks = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                chunks.append(ast.get_source_segment(content, node))
                
            elif isinstance(node, ast.ClassDef):
                # Capture the entire class definition
                chunks.append(ast.get_source_segment(content, node))
                
                # Also capture individual methods with class context
                for sub_node in node.body:
                    if isinstance(sub_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_code = ast.get_source_segment(content, sub_node)
                        chunks.append(f"Class: {node.name}\n{method_code}")
                    
        return chunks if chunks else [content]