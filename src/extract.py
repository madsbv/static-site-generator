#!/usr/bin/env python3
import re


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    # The first non-capturing group makes sure we don't accidentally match images
    pattern = r"(?:^|[^!])\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches
