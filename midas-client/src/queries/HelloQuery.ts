import { gql } from '@apollo/client';

export const GET_HELLO = gql`
  query Hello {
    hello
  }
`