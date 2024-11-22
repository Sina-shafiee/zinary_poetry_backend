import graphene
from graphql.language import ast


class Date(graphene.Scalar):
    @staticmethod
    def serialize(value):
        return value.isoformat()  # Output in ISO 8601 format

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return node.value

    @staticmethod
    def parse_value(value):
        return value
