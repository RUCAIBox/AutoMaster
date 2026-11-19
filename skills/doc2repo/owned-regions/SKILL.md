---
name: owned-regions
description: Construct structured readers by giving each parser layer ownership of one input region and its returned structure.
---

# Construct readers around owned input regions

Use this method when implementing a parser, decoder, tokenizer, or record reader
whose input contains nested groups, quoted text, delimiters, or length-framed
values. Preserve a required parsing library or native engine; implement the
repository's adapter and public objects around it. A flat format can keep a
simple scanner.

Choose one consumption convention for the core reader. For example,
`read_one(source, start, end) -> (value, next_position)` consumes exactly one
unit and leaves the following unit untouched. A shared cursor is equally valid;
make either the child or its caller advance it, never both. Define whether the
closing marker belongs to the child and keep that convention at every call site.

Build the ownership boundary into the algorithm:

- A parent recognizes an opening marker or length, delegates the interior to a
  child reader, attaches the child's result, then resumes at the returned suffix.
  The child processes a proper subregion or advances the shared cursor. It must
  not repeatedly parse the same unchanged region until a depth limit stops it.
- When building a token tree, preserve nested nodes of the same kind as well as
  mixed kinds. Counting delimiters and skipping them can find a group's end while
  losing its children. When grouping an existing token list, do not wrap a
  container's own opening and closing tokens again during recursion: process its
  interior or already identified child lists.
- Read quoted or escaped payload as a lexical unit before interpreting its
  delimiter-like characters. Keep lexical mode and source position together.
  For framed bytes, distinguish payload length from header size and resume at the
  first byte after that frame. Incremental readers retain incomplete input and
  unread suffixes according to their documented contract.

Return the representation the API specifies: an AST may preserve nested objects,
an expander may combine child alternatives, and a stream may yield one record at
a time. Do not flatten, normalize, eagerly buffer, or reject tolerated tails merely
to make the internal algorithm uniform. Required backtracking, empty matches,
malformed-input recovery and EOF behavior remain contract-specific.

Exercise the core through a public entry point using a nested unit followed by
a sibling. Inspect the expected child structure or decoded values and the sibling;
text round-tripping alone can hide an incorrect tree. Include same-kind nesting
or a quoted delimiter where applicable. For a stream, split one unit across input
chunks and then supply the next unit. Trace a mismatch to the owner that consumed,
discarded, or regrouped the wrong region; repair that handoff and rerun the case.
Continue implementing the complete repository, keeping these core readers shared
by the corresponding public entry points.
