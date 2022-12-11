#pragma once
#include <Arduino.h>
template <typename T, uint16_t QUEUE_SIZE> class CircularQueue
{
    private:
        uint16_t m_writeIndex;
        uint16_t m_readIndex;
        uint16_t m_entries;
        bool m_overwrite;
        T m_queue[QUEUE_SIZE];

    public:    
        CircularQueue(bool t_overwrite);

        uint16_t enqueue(T t_data);

        T dequeue();

        bool isFull();

        bool isEmpty();

        T queueReadAt(uint16_t t_index);

        uint16_t queueSize();

        uint16_t queueEntries();

        void queueReset();

        void printQueue();
};



/**
 * @brief Circular Queue constructor
 * 
 */
template <typename T, uint16_t QUEUE_SIZE> CircularQueue<T, QUEUE_SIZE>::CircularQueue(bool t_overwrite)
{
    m_overwrite = t_overwrite;
    queueReset();
}


/**
 * @brief Enqueue loads data to the queue, one Byte per call
 * 
 * @param[in] t_data 
 */
template <typename T, uint16_t QUEUE_SIZE> uint16_t CircularQueue<T, QUEUE_SIZE>::enqueue(T t_data)
{
    uint16_t last_insertion_index = -1;
    if(isFull() && (!m_overwrite))
    {
        Serial.println("Queue is full");
        return last_insertion_index;
    }


    m_queue[m_writeIndex] = t_data;
    if(!isFull())                                       ///Stop incrementing number of entries when queue is full
        m_entries++;
    last_insertion_index = m_writeIndex;
    m_writeIndex = (m_writeIndex+1) % QUEUE_SIZE;       ///Modulo is used so the Index "circles around" when the final cell
                                                        ///of the queue is reached
    return last_insertion_index;
}

/**
 * @brief Deqeueu unloads data from the queue, one Byte per call
 * 
 * @return char 
 */
template <typename T, uint16_t QUEUE_SIZE> T CircularQueue<T, QUEUE_SIZE>::dequeue()
{
    T data;
    if(isEmpty())
    {
        return data;
    }

    data = m_queue[m_readIndex];
    m_entries--;
    m_readIndex = (m_readIndex+1) % QUEUE_SIZE;
    return data;
     
}


/**
 * @brief Checks if the queue is full 
 * 
 * @return true 
 * @return false 
 */
template <typename T, uint16_t QUEUE_SIZE> bool CircularQueue<T, QUEUE_SIZE>::isFull()
{
    return (m_entries >= QUEUE_SIZE);                   ///if the number of entries much the size of the queue
}                                                       ///then the queue is full.


/**
 * @brief Checks if the queue is empty              
 * 
 * @return true 
 * @return false 
 */
template <typename T, uint16_t QUEUE_SIZE> bool CircularQueue<T, QUEUE_SIZE>::isEmpty()
{
    return (m_entries == 0);
}


/**
 * @brief Given an index number it will return the Byte that is stored in that cell
 * of the queue
 * 
 * @param[in] t_index corresponds to the index of the target cell
 * @return char 
 */
template <typename T, uint16_t QUEUE_SIZE> T CircularQueue<T, QUEUE_SIZE>::queueReadAt(uint16_t t_index)
{
    return m_queue[t_index];
}


/**
 * @brief Returns the size of the queue
 * //NOTE This function is not that usefull but it was created for readabillity
 * perposes
 * 
 * @return int 
 */
template <typename T, uint16_t QUEUE_SIZE> uint16_t CircularQueue<T, QUEUE_SIZE>::queueSize()
{
    return QUEUE_SIZE;
}


/**
 * @brief Return the number of entries currently stored inside the queue
 * 
 * @return int 
*/
template <typename T, uint16_t QUEUE_SIZE> uint16_t CircularQueue<T, QUEUE_SIZE>::queueEntries()
{
    return m_entries;
}

/**
 * @brief Resets the queue by reseting the queue's indexes
 * 
 */
template <typename T, uint16_t QUEUE_SIZE> void CircularQueue<T, QUEUE_SIZE>::queueReset()
{
    m_readIndex = 0;
    m_writeIndex = 0;
    m_entries = 0;
}


