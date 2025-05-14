import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Snackbar, Alert } from '@mui/material';
import { selectNotifications } from '../../store/slices/uiSlice';
import { removeNotification } from '../../store/slices/uiSlice';

const NotificationSystem: React.FC = () => {
    const dispatch = useDispatch();
    const notifications = useSelector(selectNotifications);

    const handleClose = (id: string) => {
        dispatch(removeNotification(id));
    };

    return (
        <>
            {notifications.map((notification) => (
                <Snackbar
                    key={notification.id}
                    open={true}
                    autoHideDuration={6000}
                    onClose={() => handleClose(notification.id)}
                    anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                >
                    <Alert
                        onClose={() => handleClose(notification.id)}
                        severity={notification.type}
                        sx={{ width: '100%' }}
                        elevation={6}
                        variant="filled"
                    >
                        {notification.message}
                    </Alert>
                </Snackbar>
            ))}
        </>
    );
};

export default NotificationSystem;
