import React from "react";
import styled from 'styled-components'
import { Link } from 'react-router-dom';
import palette from "../../lib/styles/palette";
import Button from '../common/Button';


// 회원가입과 로그인 폼

const StyledAuthForm = styled.div`
    h3 {
        margin: 0;
        color: ${palette.gray[8]};
        margin-bottom: 1rem;
    }
    `;
//에러 화면

const ErrorMessage = styled.div`
    color: red;
    text-align: center;
    font-size: 0.875rem;
    margin-top: 1rem;
    `;


// 스타일링 된 input

const StyledInput = styled.input`
    font-size: 1rem;
    border: none;
    border-bottom: 1px solid ${palette.gray[5]};
    padding-bottom: 0.5rem;
    outline: none;
    width: 100%
    &:focus {
        color: $oc-teal-7;
        border-bottom: 1px solid ${palette.gray[7]};
    }
    & + & {
        margin-top: 1rem;
    }
    `;

// 폼 하단 로그인 or 회원 가입 링크 보여줌

const Footer = styled.div`
    margin-top: 2rem;
    text-align: right;
    a {
        color: ${palette.gray[6]};
        text-decoration: underline;
        &:hover {
            color: ${palette.gray[9]};
            }
        }
    `;
const ButtonWithMarginTop = styled(Button)`
    margin-top: 1rem;
    `;

const textMap = {
    login: '로그인',
    signup: '회원가입',
};

const AuthForm = ({type, form, onChange, onSubmit, error }) => {
    const text = textMap[type];
    return (
        <StyledAuthForm>
            <h3>{text}</h3>
            <form onSubmit={onSubmit}>
                <StyledInput autoComplete="username" name="username" placeholder="아이디" onChange={onChange} value={form.username}/>
                <StyledInput autoComplete="new-password" name="password" placeholder="비밀번호" type="password" onChange={onChange} value={form.password} />
                {type === 'signup' && (
                    <StyledInput autoComplete="new-password" name="passwordConfirm" placeholder="비밀번호 확인" type="password" onChange={onChange} value={form.passwordConfirm} />
                    // ) && (
                    // <StyledInput autoComplete="familyname" name="familyname" placeholder="가족명" type="text" />) && (
                    // <StyledInput autoComplete="email" name="email" placeholder="이메일" type="email" />
                    // 
                    )}
                {error && <ErrorMessage>{error}</ErrorMessage>}
                <ButtonWithMarginTop cyan fullWidth style={{ marginTop: '1rem'}}>{text}</ButtonWithMarginTop>
            </form>
            <Footer>
                {type === 'login' ? ( <Link to="/signup">회원가입</Link>) : ( <Link to="/login">로그인</Link>)}
            </Footer>
        </StyledAuthForm>
    );
};

export default AuthForm;