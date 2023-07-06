use crate::lexer::SyntaxKind;
use crate::syntax::{YerLanguage, SyntaxNode};
use logos::Logos;
use rowan::{GreenNode, GreenNodeBuilder, Language};

pub(crate) struct Parser<'a> {
    lexer: logos::Lexer<'a, SyntaxKind>,
    builder: GreenNodeBuilder<'static>,
}

impl<'a> Parser<'a> {
    // add code here
    pub(crate) fn new(input: &'a str) -> Self {
        Self {
            lexer: SyntaxKind::lexer(input),
            builder: GreenNodeBuilder::new(),
        }
    }
    pub(crate) fn parse(mut self) -> Parse {
        self.start_node(SyntaxKind::Root.into());
        if self.lexer.next() == Some(SyntaxKind::Number) {
            self.builder.token(
                YerLanguage::kind_to_raw(SyntaxKind::Number),
                self.lexer.slice().into(),
            );
        }
        self.finish_node();

        Parse {
            green_node: self.builder.finish(),
        }
    }
    fn start_node(&mut self, kind: SyntaxKind) {
        self.builder.start_node(YerLanguage::kind_to_raw(kind));
    }
    fn finish_node(&mut self) {
        self.builder.finish_node();
    }
}

pub(crate) struct Parse {
    green_node: GreenNode,
}

impl Parse {
    pub fn debug_tree(&self) -> String {
        let syntax_node = SyntaxNode::new_root(self.green_node.clone());
        let formatted = format!("{:#?}", syntax_node);

        // cut off \n
        formatted[0..formatted.len() - 1].to_string()
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::syntax::SyntaxNode;

    #[test]
    fn parse_nothing() {
        let parse = Parser::new("").parse();

        assert_eq!(
            format!("{:#?}", SyntaxNode::new_root(parse.green_node)),
            r#"Root@0..0
"#,
        );
    }
}
