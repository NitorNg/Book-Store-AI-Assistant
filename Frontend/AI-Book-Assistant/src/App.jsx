import React from 'react'
import './index.css'

function App() {
  return (
    <div className='flex justify-center items-center h-screen'>
      <div className='flex flex-col justify-between border w-140 h-190 rounded-xl'>

        <div className='w-full h-20 border border-blue-500'>
          Top
        </div>
        <div className="border border-green-500 h-150">
          Middle
        </div>
        <div className='border border-red-500 h-20'>
          Bottom
        </div>

      </div>
    </div>
  )
}

export default App