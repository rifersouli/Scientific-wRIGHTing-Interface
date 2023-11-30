import React from 'react'
import Button from '@mui/joy/Button';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';
import DialogTitle from '@mui/joy/DialogTitle';
import DialogContent from '@mui/joy/DialogContent';
import Stack from '@mui/joy/Stack';

const CaixaDialogo = ({ open = false, onClose, resumo }) => {
    return (

        <Modal open={open} onClose={() => onClose(false)}>
            <ModalDialog 
              size="lg"
              color="neutral"
              variant="soft"
            >
                <ModalClose></ModalClose>
                <DialogTitle>Qual(is) das sentenças do resumo caracteriza(m) Objetivo?</DialogTitle>
                <DialogContent>{resumo.resumo}Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</DialogContent>
                <button className='BotaoNenhumaAlternativa'>
                    <h3>Nenhuma das alternativas</h3>
                </button>
                {console.log(resumo.resumo)}
            </ModalDialog>
        </Modal>

    );
};

export default CaixaDialogo;