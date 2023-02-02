// 재생할 영상이 더 이상 없을 때 띄워지는 페이지
import React from 'react';
import "./Main.css"
import Todo from '../components/Todo';
import Calendar from '../components/Calendar';
import Caption from '../components/Caption';

const Main = () => {
    return ( 
        <div>
          <div className='calendardiv'>
            <Calendar />
          </div>
          <Caption></Caption>
          <div className='tododiv'>
            <Todo />
          </div>
        </div>
     );
}
 
export default Main;