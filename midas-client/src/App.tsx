import * as React from 'react';

import {useQuery } from '@apollo/client'

import { GET_HELLO } from './queries/HelloQuery';

const Test: React.FC = () => {
  const { data, error } = useQuery(GET_HELLO)

  if (data) {
    console.log('data', data)
  }
  return (
    <>
      <div>test fc</div>
      {/* <div>
        {data}
      </div> */}
    </>
  )
}

function App() {
  return (
    <div>
      <Test />
    </div>
  );
}

export default App;
